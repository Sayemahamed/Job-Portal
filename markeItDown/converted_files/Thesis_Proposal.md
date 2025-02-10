International Islamic University Chittagong

Department of Computer Science and Engineering

A Thesis Proposal on

Optimizing Computational Resource
Requirements in Large Language
Models through Sub-Model
Architectures

Supervised by:

Dr. Muhammed Jamshed Alam Patwary
Research Assistant Professor
Department of Institute of Information and Communication Technology
Chittagong University Engineering and Technology

Submitted By:

Name

Md. Ifthekar Ahamed Sayem
Mir Md. Tarhimul Quader
Turja Dutta

Student ID
C221020
C221017
C221026

Approval of the Supervisor

Dr. Muhammed Jamshed Alam Patwary
Research Assistant Professor
Department of Institute of Information and Communication Technology
Chittagong University Engineering and Technology

1

Introduction

GPT-4, BERT, and Switch Transformers are examples of Large Language Models (LLMs),
which are important developments in Natural Language Processing (NLP). These mod-
els frequently achieve state-of-the-art performance in a wide range of tasks, such as text
production, summarization, and translation. Their unusually high computing resource
needs, however, present problems with scalability, cost, and environmental effect.

Because LLMs are being used so quickly, there is a growing need for more effective
architectures that can produce outcomes that are on par with or better while using less
computing power. Although methods like adaptive computation, modular design, and
sparse activation have showed promise, they also present new implementation, scalability,
and resource allocation issues.Through the design, development, and evaluation of a
unique sub-model architecture optimized for efficiency, this study seeks to address these
issues.

2 Thesis Motivation

This study of this research is motivated by the following important factors:

• Resource Constraints: The performance of AI is limited by the substantial com-
putational resources needed for LLM deployment and training, which are normally
out of reach for small businesses.

• Environmental Impact: LLMs’ energy usage results in carbon emissions, which

raises moral questions about their long-term viability.

• Cost Efficiency: Expanding the use of LLMs can be made possible by lowering the
price hurdles for researchers and smaller companies by reducing computing needs.

• Potential Applications: In settings with limited resources, such healthcare, edu-
cation, and disaster response systems, effective LLMs can open up new possibilities.

3 Research Background

3.1 Problem Statement

A few major challenges faced by large language models are:

1. High Resource Demands: Many users are unable to access models like GPT-4

because to their enormous computing demands.

2. Scalability Challenges: Increasing models frequently results in disproportion-

ately higher hardware expenses and requirements.

3. Implementation Issues: In order to function well, strategies like modularity and

sparse activation need efficient load balancing and synchronization.

1

3.2 Research Questions

• In what ways may sub-model structures be created to maximize LLM resource

usage?

• What compromises are there between performance of models and computational

efficiency?

• How can these structures be scaled for real-world applications and put into practice?

• Which particular deployment frameworks can improve resource-optimized LLMs’

usefulness across a range of domains?

4 Literature Review

This research builds on the theoretical foundation following works:

• Switch Transformers (Fedus et al., 2021): Demonstrated how sparse activation,
through Mixture of Experts (MoE), can reduce computational costs while scaling
up to trillions of parameters.

• Adaptive Computation Time (Graves, 2016): Introduced dynamic computation

where the depth of the model adapts based on the complexity of the input.

• Universal Transformers (Dehghani et al., 2018): Proposed a model that adjusts

the number of computation steps dynamically to optimize resource use.

• Modular Knowledge Retrieval (Lian et al., 2022): Combined modular retrieval
systems with language models for task-specific applications, highlighting the poten-
tial of modular architectures in LLMs.

• GShard (Lepikhin et al., 2020): Presented conditional computation techniques for

efficiently scaling giant models.

• Sparse Transformer Variants (Child et al., 2019): Introduced sparse attention
mechanisms to reduce the quadratic scaling of self-attention, offering additional
avenues for computational efficiency in transformers.

5 Research Gap

Despite advancements in resource-efficient architectures, the following gaps remain:

• While sparse activation models—like those which use the Mixture of Experts (MoE)
architecture—have been thoroughly investigated in theoretical and experimental
contexts (e.g., studies on sparsity, scaling, and gating processes), there is still a
large gap in applied or practical research.

• Effective deployment of sparse activation models in real-world production systems
is challenging because to issues including load balancing, communication costs,
and inference delay. Current MoE systems frequently experience load balancing
inefficiencies, resulting in poor performance as certain experts are over-utilized while
others are underused.

2

• Poor routing choices in gating methods lead to performance deterioration or needless
expert activation.It is still difficult to train the gating mechanism efficiently while
preventing bias and instability in expert selection. Dynamic gating techniques that
can adaptively route inputs based on workload needs or context are not well studied.

• It is still difficult to efficiently propagate gradients back through the experts and

gating mechanism, particularly for large-scale MoE models.

This research aims to address these gaps by proposing a novel sub-model architecture

that integrates sparse activation, modularity, and adaptive computation.

6 Research Objectives

1. Identify Limitations in Existing Architectures: Examine existing large lan-
guage model (LLM) designs in detail to identify inefficiencies pertaining to deploy-
ment issues, scalability, and resource usage, especially in sparse activation models.

2. Design and Develop a Novel MoE-Based Architecture: Develop a resource-
optimized Mixture of Experts (MoE) architecture that successfully strikes a com-
promise between computational efficiency and model performance by utilizing mod-
ularity, adaptive computing concepts, and sparse activation.

3. Explore Trade-offs Between Sparsity, Accuracy, and Cost: Analyze and
measure the trade-offs between computational costs, model accuracy, and expert
sparsity to provide guidance for resource allocation optimization in MoE designs.

4. Evaluate the Proposed Architecture: Analyze and measure the trade-offs be-
tween computational costs, model accuracy, and expert sparsity to provide guidance
for resource allocation optimization in MoE designs.

7 Methodology

7.1 Literature Review

Analyze existing sparse and modular architectures, focusing on Mixture of Experts (MoE)
models, adaptive computation, and scalability challenges. Identify gaps in current ap-
proaches to resource optimization in LLMs.

7.2 Model Design

Develop a novel sub-model architecture leveraging sparse activation, modularity, and
adaptive computation principles. Design an efficient gating mechanism for expert selec-
tion in MoE architectures.

7.3 Architecture

Describe the fundamental architecture of the suggested LLM model, including how sparse
activation techniques and MoE concepts are integrated. To maximize expert selection
depending on work requirements and input complexity, use a dynamic gating system.

3

Use modular design concepts to enable effective resource usage and scalability. Examine
hybrid compute techniques to strike a compromise between CPU/GPU efficiency and
memory use.

Figure 1: Sparse Mixture of Experts (MoE)

Figure 2: MoE Layer embedded in Transformer

7.4 Implementation

Build and train the proposed architecture using state-of-the-art frameworks such as Ten-
sorFlow or PyTorch. Implement techniques for effective load balancing and synchroniza-
tion across experts. We will examine the Mixture of Experts (MoE) architecture of the

4

recently well-known AI DeepSeek as a model to learn how it effectively activates only
pertinent subsets of parameters for given inputs, maximizing the use of computing re-
sources. Building on this framework, our research will seek to create an improved MoE
architecture that can handle issues like load balancing, training stability, and scalability
while also further lowering computational demands, making it appropriate for real-world
applications in resource-constrained settings.

Figure 3: MoE Architecture of Deepseek

7.5 Benchmarks and Evaluation Framework

The performance and efficiency of the proposed architecture will be evaluated using the
following benchmarks:

1. GLUE (General Language Understanding Evaluation): Evaluate the model’s
performance on common NLP tasks such as textual entailment, sentiment analysis,
and sentence similarity.

2. SuperGLUE: A more difficult version of GLUE that incorporates coreference res-

olution and multi-hop reasoning.

3. BIG-bench (Beyond the Imitation Game Benchmark): Accesses LLMs on
a variety of innovative activities, including as long-form writing production, inven-
tiveness, and reasoning.

4. FLOPs (Floating Point Operations): Measures the amount of floating-point

operations are needed for inference and training.

5

5. MMLU (Massive Multitask Language Understanding): Analyzes models’
capacity to generalize across 57 disciplines, including the social sciences, humanities,
and STEM.

6. Energy Consumption (PowerBench): Assesses a model’s energy efficiency dur-

ing training and inference; this is commonly expressed in kWh.

7. Expert Load Balancing: The benchmark index, which is unique to MoE mod-
els, assesses how effectively the gating mechanism divides up computation among
experts in order to reduce resource under-utilization.

8. Adversarial GLUE (AdvGLUE): Evaluates the robustness of models to adver-

sarial inputs.

9. FewRel (Few-Shot Relation Classification): Evaluates how well models per-

form on related classification tasks using sparse training data.

10. CarbonFootprint: Measures the carbon emissions associated with training and

inference.

7.6 Deployment

Validate the architecture in real-world NLP applications, such as chatbots, domain-
specific text generation, or question-answering systems. Analyze performance across
different deployment environments to assess scalability and robustness.

7.7 Research Type

Quantitative Research: Observations, experiments, and benchmarking will form the
basis of the study.

7.8 Data Sources

Datasets used for training and evaluation include WikiText, Common Crawl, and Open-
WebText.

7.9 Methods

Implement observations, experiments, and performance benchmarking to validate the
research objectives.

8 Contribution of the Work

• Innovative Sub-Model Architecture: Proposes a novel sub-model architecture
that preserves competitive performance metrics while drastically lowering comput-
ing resource needs by employing sparse activation and Mixture of Experts (MoE).

• Framework for Scalable Deployment: Develops a platform for the scalable
deployment of effective LLM applications, allowing for real-world integration across
a range of industries, including healthcare and education.

6

• Environmental Impact Mitigation: Contributes to the reduction of environ-
mental impact by optimizing energy consumption and minimizing carbon emissions
in large-scale AI model training and deployment.

• Increased Accessibility to LLMs: Enhances the accessibility of LLMs for smaller
organizations lowers financial and technical obstacles to enhance inclusion in AI re-
search by making LLMs more accessible to academics and smaller companies.

9 Expected Thesis Contribution

The contributions of this research are expected to be significant in multiple dimensions,
addressing the challenges of computational efficiency, scalability, and sustainability in
Large Language Models (LLMs):

1. Enhanced Computational Efficiency and Scalability in LLMs: This work
will help create a new Mixture of Experts (MoE) architecture that draws inspira-
tion from DeepSeek. Only the most pertinent model elements will be dynamically
activated by the suggested design, which will optimize resource allocation and cut
down on pointless calculations. This strategy will overcome constraints in terms
of cost, accessibility, and energy efficiency while allowing LLMs to scale to tackle
increasingly complicated tasks and drastically reducing computing costs.

2. Comprehensive Framework for Deploying Resource-Optimized LLMs: To
ensure that the suggested architecture can be easily included into a variety of sec-
tors, such as e-commerce, healthcare, and education, a workable deployment frame-
work will be created. The model will be appropriate for both high-resource and
resource-constrained contexts thanks to the framework’s load balancing, training
optimization, and adaptive resource management techniques. The framework will
make modern technology more accessible to everybody by lowering the infrastruc-
tural needs. LLMs for smaller organizations and researchers.

3. In-Depth Analysis of Trade-Offs Between Efficiency and Performance:
This research project will offer a thorough assessment of the compromises made
between model performance and computing economy. In order to comprehend their
impact on accuracy and resource use, variables including the quantity of specialists,
activation thresholds, and input complexity will be investigated. For scholars and
practitioners looking to create or implement effective LLMs, these insights will
provide practical recommendations.

4. Advancements in Sustainable AI Development: The research results will
support international efforts to promote sustainable AI development by drastically
lowering the energy and compute resources needed for LLM training and inference.
By proving that state-of-the-art performance can be attained while sticking to re-
sponsible energy consumption, the suggested design will serve as a model and lessen
the environmental effect of large-scale AI systems.

5. Scalability for Diverse Applications and Domains: The suggested archi-
tecture’s adaptability will allow it to be used in a variety of NLP activities and
domains, including customized recommendation systems, real-time chatbots, and

7

domain-specific text production. The architecture will be a desirable option for
businesses with different computing restrictions because to its capacity to func-
tion well in both high-resource and low-resource situations, increasing the LLMs’
worldwide reach and usefulness.

Together, these efforts seek to close the gap between state-of-the-art AI research and
its real-world applications in a variety of industries by making LLMs more affordable,
sustainable, and adaptable.

10 Work Plan

Here is our work plan:

10.1 Gantt Chart

Thesis
activities
Literature Re-
view and The-
oretical Frame-
work
Analysis
of
Modern LLM
Architectures
Problem Defi-
nition and Re-
search Objec-
tives
Architecture
Design, Devel-
opment
and
debugging
Experimental
Setup, Bench-
and
marking
change
ar-
chitecture(if
required)
Documentation
and
Thesis
Writing
Review
Revision
Final Submis-
sion and De-
fense Prepara-
tion

and

1

2

3

4

5

6

7

8

2025
Jan Feb Mar Apr May June July Aug Sept Oct Nov Dec

30%

20%

5%

15%

20%

5%

3%

2%

8

References

[1] Shaojie Cai, Ziang Jiang, Yifan Xu, Yixin Liu, and James Zou. A survey on mixture

of experts. arXiv preprint arXiv:2407.06204, 2024. Citations: 52.

[2] Aman Chadha and Arpita Vats. The evolution of mixture of experts: A survey from

basics to breakthroughs. Preprints, 2024.

[3] William Fedus, Barret Zoph, and Noam Shazeer. Switch transformers: Scaling to
trillion parameter models with simple and efficient sparsity. Journal of Machine
Learning Research, 23(120):1–39, 2022. Citations: 1,981.

[4] Szymon Jaszczur, Rahul Chowdhery, Jared Kaplan, Sharan Narang, Kamyar Aziz-
zadenesheli, Chris Ying, and Noam Shazeer. Sparse is enough in scaling transformers.
arXiv preprint arXiv:2111.06377, 2021. Citations: 93.

[5] Noam Shazeer, Azalia Mirhoseini, Krzysztof Maziarz, Andy Davis, Quoc V. Le, Geof-
frey E. Hinton, and Jeff Dean. Outrageously large neural networks: The sparsely-gated
mixture-of-experts layer. arXiv preprint arXiv:1701.06538, 2017. Citations: 2,596.

[1] [2] [3] [4] [5]

9

