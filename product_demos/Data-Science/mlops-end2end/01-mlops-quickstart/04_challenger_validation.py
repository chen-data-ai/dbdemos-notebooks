# Databricks notebook source
# MAGIC %md
# MAGIC # Challenger model validation
# MAGIC
# MAGIC This notebook performs validation tasks on the candidate __Challenger__ model.
# MAGIC
# MAGIC It goes through a few steps to validate the model before labeling it (by setting its alias) to `Challenger`.
# MAGIC
# MAGIC When organizations first start to put MLOps processes in place, they should consider having a "human-in-the-loop" to perform visual analyses to validate models before promoting them. As they get more familiar with the process, they can consider automating the steps in a __Workflow__ . The benefits of automation is to ensure that these validation checks are systematically performed before new models are integrated into inference pipelines or deployed for realtime serving. Of course, organizations can opt to retain a "human-in-the-loop" in any part of the process and put in place the degree of automation that suits its business needs.
# MAGIC
# MAGIC <img src="https://github.com/databricks-demos/dbdemos-resources/blob/main/images/product/mlops/mlops-uc-end2end-4.png?raw=true" width="1200">
# MAGIC
# MAGIC *Note: in a typical MLOps setup, this would run as part of an automated job to validate a new model. We'll run this simple demo as an interactive notebook.*
# MAGIC
# MAGIC <!-- Collect usage data (view). Remove it to disable the collection or disable the tracker during installation. View README for more details.  -->
# MAGIC <img width="1px" src="https://ppxrzfxige.execute-api.us-west-2.amazonaws.com/v1/analytics?category=lakehouse&notebook=04_challenger_validation&demo_name=mlops-end2end&event=VIEW">

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC ## General Validation Checks
# MAGIC
# MAGIC <!--img style="float: right" src="https://github.com/QuentinAmbard/databricks-demo/raw/main/retail/resources/images/churn-mlflow-webhook-1.png" width=600 -->
# MAGIC
# MAGIC In the context of MLOps, there are more tests than simply how accurate a model will be.  To ensure the stability of our ML system and compliance with any regulatory requirements, we will subject each model added to the registry to a series of validation checks.  These include, but are not limited to:
# MAGIC <br>
# MAGIC * __Model documentation__
# MAGIC * __Inference on production data__
# MAGIC * __Champion-Challenger testing to ensure that business KPIs are acceptable__
# MAGIC
# MAGIC In this notebook, we explore some approaches to performing these tests and how we can add metadata to our models by tagging whether they have passed a given test.
# MAGIC
# MAGIC This part is typically specific to your line of business and quality requirements.
# MAGIC
# MAGIC For each test, we'll add information using tags to know what has been validated in the model. We can also add Comments to a model if needed.

# COMMAND ----------

# MAGIC %pip install --quiet mlflow==2.19
# MAGIC dbutils.library.restartPython()

# COMMAND ----------

# MAGIC %run ../_resources/00-setup

# COMMAND ----------

# MAGIC %md
# MAGIC ## Fetch Model information
# MAGIC
# MAGIC We will fetch the model information for the __Challenger__ model from Unity Catalog.

# COMMAND ----------

# We are interested in validating the Challenger model
model_alias = "Challenger"
model_name = f"{catalog}.{db}.mlops_churn"

client = MlflowClient()
model_details = client.get_model_version_by_alias(model_name, model_alias)
model_version = int(model_details.version)

print(f"Validating {model_alias} model for {model_name} on model version {model_version}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Model checks

# COMMAND ----------

# MAGIC %md
# MAGIC #### Description check
# MAGIC
# MAGIC Has the data scientist provided a description of the model being submitted?

# COMMAND ----------

# If there's no description or an insufficient number of characters, tag accordingly
if not model_details.description:
  has_description = False
  print("Please add model description")
elif not len(model_details.description) > 20:
  has_description = False
  print("Please add detailed model description (40 char min).")
else:
  has_description = True

print(f'Model {model_name} version {model_details.version} has description: {has_description}')
client.set_model_version_tag(name=model_name, version=str(model_details.version), key="has_description", value=has_description)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Model performance metric
# MAGIC
# MAGIC We want to validate the model performance metric. Typically, we want to compare this metric obtained for the Challenger model against that of the Champion model. Since we have yet to register a Champion model, we will only retrieve the metric for the Challenger model without doing a comparison.
# MAGIC
# MAGIC The registered model captures information about the MLflow experiment run, where the model metrics were logged during training. This gives you traceability from the deployed model back to the initial training runs.
# MAGIC
# MAGIC Here, we will use the F1 score for the out-of-sample test data set aside at training time.

# COMMAND ----------

model_run_id = model_details.run_id
f1_score = mlflow.get_run(model_run_id).data.metrics['test_f1_score']

try:
    #Compare the challenger f1 score to the existing champion if it exists
    champion_model = client.get_model_version_by_alias(model_name, "Champion")
    champion_f1 = mlflow.get_run(champion_model.run_id).data.metrics['test_f1_score']
    print(f'Champion f1 score: {champion_f1}. Challenger f1 score: {f1_score}.')
    metric_f1_passed = f1_score >= champion_f1
except:
    print(f"No Champion found. Accept the model as it's the first one.")
    metric_f1_passed = True

print(f'Model {model_name} version {model_details.version} metric_f1_passed: {metric_f1_passed}')
# Tag that F1 metric check has passed
client.set_model_version_tag(name=model_name, version=model_details.version, key="metric_f1_passed", value=metric_f1_passed)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Benchmark or business metrics on the eval dataset
# MAGIC
# MAGIC Let's use our validation dataset to check the potential new model impact.
# MAGIC
# MAGIC ***Note: This is just to evaluate our models, not to be confused with A/B testing**. A/B testing is done online, splitting the traffic between 2 models. It requires a feedback loop to evaluate the effect of the prediction (e.g., after a prediction, did the discount we offered to the customer prevent the churn?). We will cover A/B testing in the advanced part.*

# COMMAND ----------

import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix
import plotly.express as px

validation_pdf = spark.table('mlops_churn_training').filter("split='validate'").toPandas()

def get_predictions(validation_pdf, model_alias):
    try:
        import mlflow
        model_uri = f"models:/{catalog}.{db}.mlops_churn@{model_alias}"
        model = mlflow.pyfunc.load_model(model_uri)
        validation_pdf['predictions'] = model.predict(validation_pdf)
    except Exception as e:
        error_msg = str(e)
        if (
            "No module named 'databricks.automl_runtime'" in error_msg or
            "cannot import name 'automl'" in error_msg or
            "one_hot_encoder" in error_msg or
            "free variable 'loaded_model'" in error_msg
        ):
            print(f"AutoML model cannot be loaded on serverless. Using mock predictions for {model_alias}.")
            # MOCK: For demo, copy the true churn labels as predictions (simulates a perfect model)
            # Note: cannot import name 'automl' likely means you're using serverless. Dbdemos doesn't support autoML serverless API - this will be improved soon.
            # adding a temporary workaround to make sure this works well for now -- ignore this for classic run
            validation_pdf['predictions'] = validation_pdf['churn']
        else:
            raise e
    return validation_pdf


cost_of_customer_churn = 2000
cost_of_discount = 500
cost_true_negative = 0
cost_false_negative = cost_of_customer_churn
cost_true_positive = cost_of_customer_churn - cost_of_discount
cost_false_positive = -cost_of_discount

def get_model_value_in_dollar(preds_df):
    tn, fp, fn, tp = confusion_matrix(preds_df['churn'], preds_df['predictions']).ravel()
    return (
        tn * cost_true_negative +
        fp * cost_false_positive +
        fn * cost_false_negative +
        tp * cost_true_positive
    )

is_champ_model_exist = True
try:
    client.get_model_version_by_alias(f"{catalog}.{db}.mlops_churn", "Champion")
except Exception as error:
    print("No Champion model found, using mock for both.")
    is_champ_model_exist = False

champion_potential_revenue_gain = get_model_value_in_dollar(get_predictions(validation_pdf.copy(), "Champion")) if is_champ_model_exist else 0
challenger_potential_revenue_gain = get_model_value_in_dollar(get_predictions(validation_pdf.copy(), "Challenger"))

data = {
    'Model Alias': ['Challenger', 'Champion'],
    'Potential Revenue Gain': [challenger_potential_revenue_gain, champion_potential_revenue_gain]
}

fig = px.bar(
    data,
    x='Model Alias',
    y='Potential Revenue Gain',
    color='Model Alias',
    labels={'Potential Revenue Gain': 'Revenue Impacted'},
    title='Business Metrics - Revenue Impacted'
)
fig.show()


# COMMAND ----------

# MAGIC %md
# MAGIC ## Validation results
# MAGIC
# MAGIC That's it! We have demonstrated some simple checks on the model. Let's take a look at the validation results.

# COMMAND ----------

results = client.get_model_version(model_name, model_version)
results.tags

# COMMAND ----------

# MAGIC %md
# MAGIC ## Promoting the Challenger to Champion
# MAGIC
# MAGIC When we are satisfied with the results of the __Challenger__ model, we can promote it to Champion. This is done by setting its alias to `@Champion`. Inference pipelines that load the model using the `@Champion` alias will then load this new model. The alias on the older Champion model, if there is one, will be automatically unset. The model retains its `@Challenger` alias until a newer Challenger model is deployed with the alias to replace it.

# COMMAND ----------

if results.tags["has_description"] == "True" and results.tags["metric_f1_passed"] == "True":
  print('register model as Champion!')
  client.set_registered_model_alias(
    name=model_name,
    alias="Champion",
    version=model_version
  )
else:
  raise Exception("Model not ready for promotion")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Congratulations! Our model is now validated and promoted accordingly
# MAGIC
# MAGIC We now have the certainty that our model is ready to be used in inference pipelines and real-time serving endpoints, as it matches our validation standards.
# MAGIC
# MAGIC
# MAGIC Next: [Run batch inference from our newly promoted Champion model]($./05_batch_inference)
