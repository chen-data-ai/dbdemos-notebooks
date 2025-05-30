# Databricks notebook source
# MAGIC %md
# MAGIC # Databricks AI/BI for Understanding your Sales Pipeline
# MAGIC
# MAGIC [Databricks AI/BI](https://www.youtube.com/watch?v=5ctfW6Ac0Ws), the newest addition to the Databricks Intelligence Platform, is a new type of business intelligence product built to democratize analytics and insights for anyone in your organization - technical or nontechnical. 
# MAGIC
# MAGIC Powered by _your own organization's data,_ AI/BI understands your unique business concepts, challenges, and areas of opportunity, continuously learning and improving based on feedback - all behind a slick, nontechnical UI.
# MAGIC
# MAGIC AI/BI features two complementary capabilities: _Dashboards and Genie_. 
# MAGIC
# MAGIC - **Dashboards** provide a low-code experience to help analysts quickly build highly interactive data visualizations for their business teams using any natural language.
# MAGIC - **Genie** allows business users to converse with their data to ask questions and self-serve their own analytics.
# MAGIC
# MAGIC Databricks AI/BI is native to the Databricks Data Intelligence Platform, providing instant insights at massive scale while ensuring unified governance and fine-grained security are maintained across the entire organization.
# MAGIC
# MAGIC
# MAGIC
# MAGIC <!-- Collect usage data (view). Remove it to disable collection or disable tracker during installation. View README for more details.  -->
# MAGIC <img width="1px" src="https://ppxrzfxige.execute-api.us-west-2.amazonaws.com/v1/analytics?category=aibi&notebook=AI-BI-Sales-pipeline-review&demo_name=sales-pipeline&event=VIEW">

# COMMAND ----------

# MAGIC %md
# MAGIC # Sales Pipeline Review & Management
# MAGIC ---
# MAGIC
# MAGIC ## The Challenge
# MAGIC
# MAGIC In today’s competitive market, efficiently managing the sales pipeline is crucial across industries. Ineffective sales pipeline management can lead to missed opportunities, inaccurate revenue forecasting, and poor resource allocation. Organizations without a comprehensive data intelligence platform often struggle to consolidate data from multiple sources, deliver real-time insights to stakeholders, and reduce time-to-insights necessary for strategic adjustments in the sales process.
# MAGIC
# MAGIC ## The Solution
# MAGIC
# MAGIC Databricks' Intelligence Platform leverages **AI and Business Intelligence (or as we call it, AI/BI)** to provide seamless access to your organization's sales data. By integrating data from various CRM, marketing, and transactional sources into a unified environment, Databricks breaks down data silos and offers end-to-end visibility into the entire sales pipeline.
# MAGIC
# MAGIC Advanced AI-driven analytics and intuitive BI tools empower both technical and non-technical users to examine sales trends, forecast revenue, and analyze pipeline health through natural language queries. This accessibility accelerates time-to-insights, enhances cross-functional collaboration, and enables leadership to make informed, data-driven decisions to improve sales strategy, close rates, and overall pipeline efficiency.
# MAGIC
# MAGIC ## This Notebook
# MAGIC
# MAGIC This notebook will guide you, the knowledgeable Databricks aficionado, through deploying a Databricks AI/BI project focused on sales pipeline review and management. Follow the step-by-step process to familiarize yourself with the project. By installing this project, its dashboard and Genie Dataroom are already accessible at **these links**.
# MAGIC
# MAGIC In the following sections, this notebook will guide you through at a high level:
# MAGIC 1. Data Ingestion with **Lakeflow Connect**
# MAGIC 2. Data Governance and Security with **Unity Catalog**
# MAGIC 3. Creating Interactive **Dashboards** with Databricks
# MAGIC 4. Utilizing **Genie** for natural language queries to analyze and review your sales pipeline data, even in complex scenarios

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC ## Step 1: Utilize Lakeflow Connect for Intuitive Data Ingestion
# MAGIC
# MAGIC <div style="background-color: #1B3139; color: #F9F7F4; padding: 40px; max-width: 400px; text-align: center; border-radius: 12px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); float:right; margin: 0px 15px 0px 15px">
# MAGIC   <div style="font-size: 1.5em; color: #FFAB00; margin-bottom: 20px;">Data Ingestion with LakeFlow Connect</div>
# MAGIC   <p style="font-size: 1em; color: #EEEDE9; margin-bottom: 20px; line-height: 1.6;">
# MAGIC     Discover how to seamlessly ingest your data with LakeFlow Connect. Dive into our interactive tour to learn more!
# MAGIC   </p>
# MAGIC   <a href="https://app.getreprise.com/launch/BXZY58n/" target="_blank" style="background-color: #00A972; color: #F9F7F4; border: none; padding: 15px 25px; border-radius: 8px; font-size: 1em; font-weight: bold; text-decoration: none; display: inline-block; transition: background-color 0.3s ease; cursor: pointer;"
# MAGIC      onmouseover="this.style.backgroundColor='#FF3621';" onmouseout="this.style.backgroundColor='#00A972';">
# MAGIC     Open the Interactive Tour
# MAGIC   </a>
# MAGIC </div>
# MAGIC
# MAGIC As in any data project, your first step is to ingest and centralize your data to a central place.
# MAGIC
# MAGIC Databricks makes this super simple with LakeFlow Connect, a **point-and-click data ingestion solution** supporting:
# MAGIC
# MAGIC - Databases -- including SQL Servers and more.
# MAGIC - Entreprise application such as Salesforce, Workday, Google Analytics or ServiceNow.
# MAGIC
# MAGIC If you want to know more about LakeFlow Connect and how to incrementally synchronize your external table to Databricks, you can open the [Lakeflow Connect Product Tour](https://www.databricks.com/resources/demos/tours/platform/discover-databricks-lakeflow-connect-demo).
# MAGIC
# MAGIC
# MAGIC In this demo, we pre-loaded the data for you! For more details on how to simplify data transformation, [open the Delta Live Table Product Tour](https://www.databricks.com/resources/demos/tours/data-engineering/delta-live-tables).
# MAGIC

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC ## Step 2: Ensure data governance and security coverage with Databricks Unity Catalog
# MAGIC
# MAGIC <img src="https://raw.githubusercontent.com/databricks-demos/dbdemos-resources/refs/heads/main/images/aibi/dbx_aibi_uc.png" style="float: right; margin: 10px" width="500px">
# MAGIC
# MAGIC Once your data is ingested and ready-to-go, **Databricks Unity Catalog** provides all the key features to support your business' data governane requirements, _including but not limited to_:
# MAGIC
# MAGIC - **Fine Grained Access control on your data**: Control who can access which row or column based on your own organization
# MAGIC - **Full lineage, from data ingestion to ML models**: Analyze all downstream impact for any legal / privacy requirements
# MAGIC - **Audit and traceability**: Analyze who did what, when
# MAGIC - **Support for all data assets**: Including files, table, dashboards, ML/AI models, jobs, and more! _Simplify governance, support all your teams in one place._
# MAGIC
# MAGIC Explore the data and table ingested in [Unity Catalog](/explore/data) and make sure that it looks appropriate for your organization's needs.
# MAGIC
# MAGIC Click [here](https://www.databricks.com/product/unity-catalog) for more information on Databricks Unity Catalog.
# MAGIC

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC ## Step 3: Utilize Databricks Dashboards to clearly show data trends
# MAGIC
# MAGIC <img src="https://raw.githubusercontent.com/databricks-demos/dbdemos-resources/refs/heads/main/images/aibi/dbx_aibi_dashboard_product.gif" style="float: right; margin: 10px" width="500px">
# MAGIC
# MAGIC Your Marketing Campaign data is now available for your Data Analyst to explore and track their main KPIs.
# MAGIC
# MAGIC AI/BI Dashboards make it easy to create and iterate on visualizations with natural language through AI-assisted authoring. 
# MAGIC
# MAGIC Dashboards offers advanced data visualization capabilities including sleek charts, interactions such as cross-filtering, periodic snapshots via email, embedding and _much more_. 
# MAGIC
# MAGIC And they live side-by-side with your data, delivering instant load and rapid interactive analysis — no matter the data or user scale.
# MAGIC
# MAGIC
# MAGIC Open the <a dbdemos-dashboard-id="sales-pipeline" href='/sql/dashboardsv3/02ef00cc36721f9e1f2028ee75723cc1' target="_blank">Sales Pipeline Dashboard to analyze & track main KPIs</a>

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC
# MAGIC ## Step 4: Create Genie to allow end-users to converse with your data
# MAGIC
# MAGIC <img src="https://raw.githubusercontent.com/databricks-demos/dbdemos-resources/refs/heads/main/images/aibi/dbx_aibi_genie_product.gif" style="float: right; margin: 10px" width="500px">
# MAGIC
# MAGIC Our data is now available as a Dashboard that our business users can open.
# MAGIC
# MAGIC However, they'll likely have extra questions or followup based on the insight they see in the dashboard, like: "What the heck is wrong with my campaign, anyway?" or "What was the CTR of my campaign last month?"
# MAGIC
# MAGIC Open the <a dbdemos-genie-id="sales-pipeline" href='/genie/rooms/01ef775474091f7ba11a8a9d2075eb58' target="_blank">Sales Pipeline Genie space to deep dive into your data</a>

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ## "I've had enough of AI/BI for now, what next?"
# MAGIC
# MAGIC We have seen how Databricks' Data Intelligence Platform comprehensively understands your data, streamlining the journey from data ingestion to insightful dashboards, and supporting natural language queries.
# MAGIC
# MAGIC In addition, Databricks offers advanced capabilities, including:
# MAGIC
# MAGIC - **Data Engineering**: Build and orchestrate sophisticated data pipelines using Python and SQL
# MAGIC - **Data Quality & Monitoring**: Ensure your data remains accurate and reliable
# MAGIC - **Comprehensive Governance**: Implement fine-grained access controls and tagging
# MAGIC - **State-of-the-Art Warehouse Engine**: Achieve excellent total cost of ownership (TCO)
# MAGIC - **Support for ML, AI & GenAI Applications**: Fully hosted by Databricks
# MAGIC - **GenAI Capabilities**: Create custom agents to further empower your business users
# MAGIC
# MAGIC Interested in learning more? [Explore our end-to-end platform demos](https://www.databricks.com/resources/demos/tutorials?itm_data=demo_center) to see step-by-step implementations.
