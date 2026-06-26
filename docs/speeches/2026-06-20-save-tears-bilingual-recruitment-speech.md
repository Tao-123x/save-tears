# Save Tears UK Core Team Recruitment Speech

> Delivery: speak the English sections only. The Chinese sections are for rehearsal.

## Slide 1 — We Built It. Now We Need You.

### English

Good afternoon. We are Save Tears, a team building a smarter greywater-saving system. We started during the winter camp. Today, we have a working web product with our own domain and server. But a live website is only the beginning. To build the next stage, we need people who want to solve real engineering problems with us. [Pause]

### 中文对照

大家下午好。我们是 Save Tears，一个正在开发智能灰水节水系统的学生团队。项目最初只是冬令营期间的一个想法，如今我们已经拥有可以运行的网页产品、自己的域名和服务器。但网站上线只是开始。为了进入下一阶段，我们需要愿意和我们一起解决真实工程问题的同学。

## Slide 2 — From Winter Camp to a Live Product

### English

This slide shows our progress. First, we formed the idea and built a prototype during the winter camp. Then we developed the frontend and backend and connected them into one product. Finally, we deployed it online. The public entry page was checked again in June and was reachable. We have moved from an idea to delivery. Now we must prove that the system can work with real data and in a wider environment. [Next slide]

### 中文对照

这一页展示了我们的发展过程。首先，我们在冬令营期间形成想法并完成原型；之后，我们开发了前端和后端，把它们连接成一个完整产品；最后，我们把系统部署到了线上。公开入口页面在六月再次检查时可以正常访问。我们已经证明自己能把想法做成产品，下一步则要证明系统可以使用真实数据，并能在更广泛的环境中运行。

## Slide 3 — Three Challenges We Cannot Solve Alone

### English

We now face three clear challenges. First, international deployment: we want to test Save Tears outside China and understand a different technical environment. Second, real-world data: we have a ThingCloud-compatible backend endpoint, but real devices are not connected yet. Third, greywater-aware AI: the system must consider both tap water and reusable greywater, including where greywater is safe to use and how much should replace tap water. These are not presentation ideas. They are real areas that new members can own. [Pause]

### 中文对照

现在我们面临三个明确的挑战。第一是海外部署：我们希望在中国以外测试 Save Tears，并了解不同的技术环境。第二是真实数据：我们已经有兼容 ThingCloud 的后端接口，但真实设备尚未接入。第三是理解灰水的人工智能：系统必须同时考虑自来水和可重复利用的灰水，包括灰水可以安全用在哪里，以及应当替代多少自来水。这些不是为了展示而提出的概念，而是新成员可以真正负责的工作。

## Slide 4 — Our First AI Result

### English

We have completed one machine-learning experiment. Using public normal-water data from 810 households and 131,220 samples, we used the previous six hours of water use to predict demand in the next hour. Among five models, Random Forest performed best, with an R-squared value of 0.7498. [Point to the chart] This is a useful baseline, but it does not use real Save Tears greywater data, and weather and temperature are not current model inputs. Our next job is to improve the data, not simply make the model sound more intelligent.

### 中文对照

我们已经完成了第一个机器学习实验。我们使用来自 810 个家庭、共 131,220 条样本的公开正常用水数据，根据前六小时的用水情况预测下一小时的需求。在五种模型中，随机森林表现最好，决定系数 R² 为 0.7498。这个结果为我们提供了有价值的预测基线，但我们必须诚实说明它的局限：实验没有使用 Save Tears 的真实灰水数据，目前的模型输入也不包括天气和温度。下一步真正重要的是改进数据，而不是只让模型听起来更智能。

## Slide 5 — Why Generic LLMs Are Not Enough

### English

Forecasting demand is only one part of the problem. A generic open-source language model can discuss saving tap water, but it may invent an unsafe or unrealistic greywater ratio. Our solution separates decisions from language. First, forecasting estimates demand. Then deterministic rules, or an optimiser, decide permitted uses, available greywater, safety limits, and the replacement ratio. RAG retrieves trusted knowledge for the situation. The LLM explains the plan in clear, personal language; it does not choose the ratio. This is still a research direction, requiring real examples and a measurable evaluation set before fine-tuning. [Pause]

### 中文对照

预测需求只是问题的一部分。通用开源大语言模型通常可以讨论如何节约自来水，但它可能编造不安全或不现实的灰水使用比例。我们的方案把“做决定”和“生成语言”分开。首先由预测模型估计需求；然后由确定性规则或优化器决定允许的用途、可用灰水量、安全限制和替代比例；RAG 为当前情况检索可信知识；最后，大语言模型用清晰、个性化的语言解释计划，而不是自己决定灰水比例。这套架构目前仍是研究方向，在微调之前还需要真实案例和可衡量的评估数据集。

## Slide 6 — Two Majors, One Working System

### English

This is why we are recruiting from two majors. Telecom Engineering students can own sensors, gateways, ThingCloud integration, and data reliability. Software Engineering students can own international deployment, the backend data pipeline, forecasting, planning logic, and the user experience. These are different responsibilities, but they must become one working system: devices create reliable data, software turns that data into a safe decision, and users receive a plan they can actually follow.

### 中文对照

这就是我们同时招募两个专业同学的原因。电信工程学生可以负责传感器、网关、ThingCloud 集成和数据可靠性；软件工程学生可以负责海外部署、后端数据管线、预测、计划逻辑和用户体验。两边的职责不同，但最终必须形成一个完整系统：设备产生可靠数据，软件把数据转化为安全决策，用户获得真正能够执行的计划。

## Slide 7 — Join the Core Team

### English

Today, we are looking for 2–4 long-term core members, not temporary helpers. If you join, you will not be given a small practice task. You will own an important part of a product that already exists: deploying internationally, connecting real data, or building responsible dual-source intelligence. The selection happens here today. If you want to build something real with Telecom and Software Engineering working together, choose Save Tears. Thank you. [Pause and look at the audience]

### 中文对照

今天，我们希望招募 2–4 名长期核心成员，而不是临时帮手。加入后，你不会只得到一个简单的练习任务，而是会负责一个已经真实存在的产品中的重要部分：进行海外部署、接入真实数据，或构建负责任的双水源智能系统。选择将在今天现场进行。如果你希望电信工程与软件工程真正协作，做出一个真实产品，请选择 Save Tears。谢谢大家。
