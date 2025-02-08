# 🚀 Event Scheduler App  
A **serverless event notification system** that schedules tasks and sends email notifications at a specified time using **AWS Lambda, API Gateway, DynamoDB, EventBridge, and SNS.**  

![Architecture Diagram]

![diagram-export-2-7-2025-1_46_13-PM](https://github.com/user-attachments/assets/023ca375-810b-4380-bf78-e35a00f567ad)

---

## **🔹 Features**  
✅ **Serverless & Scalable** – Uses AWS Lambda & EventBridge for efficient scheduling.  
✅ **Automated Notifications** – Sends emails via **AWS SNS** at the scheduled time.  
✅ **API-Driven** – Frontend interacts with **API Gateway & Lambda** for seamless integration.  
✅ **DynamoDB for Storage** – Keeps track of scheduled events.  
✅ **Easy Deployment** – Deploy with AWS SAM or CDK.  

---

## **⚙️ Architecture Overview**  
1️⃣ **Frontend UI (S3 + Amplify)** – User enters event details.  
2️⃣ **API Gateway + Lambda** – Processes event submission.  
3️⃣ **DynamoDB Storage** – Saves event details.  
4️⃣ **EventBridge Scheduler** – Triggers Lambda at scheduled time.  
5️⃣ **Lambda + SNS** – Sends email notification to the user.  

---

## **🔧 How It Works**  
1️⃣ User submits event details via frontend UI.
2️⃣ API Gateway receives the request & triggers Lambda.
3️⃣ Lambda stores event data in DynamoDB & schedules it on EventBridge.
4️⃣ EventBridge triggers a second Lambda at the scheduled time.
5️⃣ Lambda sends an email notification using SNS.


To Watch the Full Walkthrough:
