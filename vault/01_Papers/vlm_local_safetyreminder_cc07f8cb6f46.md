---
title: "safetyreminder"
source_type: "original_local_pdf"
source_path: "/Users/aryamandev/Developer/blissful-bose/presentation/paper_pdfs/safetyreminder.pdf"
source_sha256: "cc07f8cb6f461fa1731f86c4867e4bc27c1004c66807d80eb62a13fdc2f57ba9"
project: "vlm-safety"
full_pdf_ingested: "True"
page_count: "14"
pages_with_extracted_text: "14"
bibliographic_metadata_verified: "False"
visual_review_completed: "False"
---
Private, Efficient and Scalable Kernel Learning
for Medical Image Analysis
Anika Hannemann1,2,∗, Arjhun Swaminathan3,4,∗, Ali Burak Ünal3,4, and Mete
Akgün3,4
1 Department of Computer Science, Leipzig University, Leipzig, Germany
2 Center for Scalable Data Analytics and Artificial Intelligence (ScaDS.AI)
Dresden/Leipzig, Germany
3 Medical Data Privacy and Privacy-preserving Machine Learning (MDPPML),
University of Tübingen, Tübingen, Germany
4 Institute for Bioinformatics and Medical Informatics (IBMI), University of
Tübingen, Tübingen, Germany
anika.hannemann@cs.uni-leipzig.de, arjhun.swaminathan@uni-tuebingen.de
Abstract. Medical imaging is key in modern medicine. From magnetic
resonance imaging (MRI) to microscopic imaging for blood cell detec-
tion, diagnostic medical imaging reveals vital insights into patient health.
To predict diseases or provide individualized therapies, machine learn-
ing techniques like kernel methods have been widely used. Nevertheless,
there are multiple challenges for implementing kernel methods. Medical
image data often originates from various hospitals and cannot be com-
bined due to privacy concerns, and the high dimensionality of image data
presents another significant obstacle. While randomised encoding offers
a promising direction, existing methods often struggle with a trade-off
betweenaccuracyandefficiency.Addressingtheneedforefficientprivacy-
preserving methods on distributed image data, we introduce OKRA (Or-
thonormal K-fRAmes), a novel randomized encoding-based approach for
kernel-based machine learning. This technique, tailored for widely used
kernel functions, significantly enhances scalability and speed compared
to current state-of-the-art solutions. Through experiments conducted on
various clinical image datasets, we evaluated model quality, computa-
tional performance, and resource overhead. Additionally, our method
outperforms comparable approaches.
Keywords: Distributed Learning· Kernel Methods · Privacy · Machine
Learning · Medical Images
1 Introduction
Medical imaging is crucial in modern medicine, offering insights into the hu-
man body and revolutionizing healthcare by aiding in disease detection, treat-
ment planning, and patient monitoring. Kernel-based machine learning, or kernel
* These authors contributed equally to this work.
arXiv:2410.15840v1  [cs.CR]  21 Oct 2024

2 A. Hannemann and A. Swaminathan et al.
learning, has become widely accepted in medical image analysis for identifying
complex patterns by mapping data to higher-dimensional spaces [28,21]. Tech-
niques like kernel-based Support Vector Machines (SVM), Principal Component
Analysis(PCA),CanonicalCorrelationAnalysis(CCA),Gaussianprocesses,and
k-means are particularly effective for smaller [13], high-dimensional datasets and
offer greater interpretability [28].
However, medical data is often distributed across various institutions, compli-
catingtheimplementationofkernellearningduetoprivacyrisks.Healthdatacan
re-identify individuals [14], and regulations like GDPR prohibit sharing sensitive
data. To tackle this, privacy preserving techniques could be employed. However,
traditional privacy techniques, such as Homomorphic Encryption (HE) [15] and
Secure Multiparty Computation (SMPC) [34], face operational challenges, while
Differential Privacy (DP) introduces model inaccuracies [4,19].
Moreover, many healthcare institutions rely on cloud services for computa-
tional tasks [2]. With this in mind, our work proposes kernel-based learning on
distributed medical data within a federated architecture using a semi-honest
central server. This approach aligns with real-world scenarios where institutions
aim to perform joint analysis for higher accuracy while maintaining data privacy
and lacking on-premise computational resources. Specifically, we employ a one-
shot federated learning approach, where a global model is computed in a single
communication round [18,17].
This method ensures the central server cannot derive sensitive information
from the data. We introduce OKRA (Orthonormal K-fRAmes), which uses ran-
domized encoding to project input data into higher-dimensional spaces. This
facilitates the training of kernel learning models as if the data were centralized,
with lower computational and communication costs compared to traditional pri-
vacy techniques. Unlike the comparable state-of-the-art solutions, OKRA re-
quires less computation time, especially for high-dimensional data.
We make three contributions:
1. We present the OKRA methodology to privately compute kernel functions
on distributed data.
2. We report a privacy analysis confirming the ability of OKRA to maintain
the privacy of both input data and the size of medical images.
3. We evaluate OKRA through extensive experimentation involving various
combinations of datasets, kernels and Machine Learning techniques.
Paper structure: Section 2 introduces related work. Section 3 describes our
methodology, followed by a privacy analysis in Section 4. Section 5 presents our
experimental results, followed by conclusion in Section 6.
2 Related Work
2.1 One-shot Federated Learning
Federated Learning (FL) [24] allows distributed nodes to train models on local
data while preserving privacy. In traditional FL, nodes iteratively share local

Private, Efficient and Scalable Kernel Learning for Medical Image Analysis 3
model parameters with a central server, which aggregates them to form a global
model. However, this iterative communication introduces latency and security
risks, such as data/model poisoning and membership inference attacks [25].
In contrast, one-shot federated learning approaches such as [18], restrict com-
munication to a single round. Each participant sends its relevant parameters to
the central server once, which subsequently undertakes the role of model train-
ing. For our methodology, the central server computes relevant kernels with a
single round of communication.
2.2 Privacy Preserving Techniques
FL incorporates various techniques to safeguard the privacy of input data:
Cryptography-based Approaches: These primarily constitute the usage of HE
and SMPC. HE aims to protect privacy of aggregated models by encrypting
the parameters of the local models. However, this is computationally intensive,
often leading to slower processing speeds, which can be a bottleneck in real-time
applications [12]. Meanwhile, SMPC splits the data into secret shares distributed
among participants for shared computation. Despite being less computationally
intensive compared to HE, it requires continuous communication, often resulting
in high execution times [26,7].
Differential Privacy:FL methods using DP introduce noise to individual models
to enhanceprivacy, makingit challenging todeducethe originalmodel oridentify
a specific data point’s membership. However, the noise added is irremovable and
often impacts model accuracy [1,4,19].
Randomized Encoding-based Approaches:Contrary to more computationally de-
manding approaches, these methods present an efficient way of preserving data
privacy, such as maintaining relationships between dot products [8,31]. Random-
ized encoding approaches [3,9,23,30] use a variety of techniques, including but
notlimitedtogeometricperturbations.Geometricperturbationsintroducestruc-
tured noise to the data. This noise can be factored out, thus differing from dif-
ferential privacy methods in the context of preserving model accuracy. It should
be noted that the security of randomized encoding-based approaches is depen-
dent on the specific problem at hand since they are tailored to meet the unique
demands and constraints of a privacy-preserving task.
2.3 Privacy-preserving Kernel Learning using Randomized
Encoding
The integration of randomized encoding methods into kernel learning presents a
promising avenue, particularly in their cost-effectiveness compared to traditional
approaches. This subsection delves into two noteworthy contributions in this
domain that achieve exact model predictions: ESCAPED [32] and FLAKE [20],
each offering distinct methodologies and implications.

4 A. Hannemann and A. Swaminathan et al.
ESCAPED makes use of randomized encoding within a multi-party compu-
tational framework for kernel computations. Its core innovation lies in enabling
secure, collaborative computing without compromising individual data privacy.
However, this approach necessitates intricate communication channels among all
participatingdataproviders.Thisrequirementbecomesparticularlycumbersome
with the introduction of new data entities, posing significant logistical challenges
in scalable deployments. On the other hand, FLAKE works towards optimizing
communication overhead in kernel-based learning. It employs a one-shot feder-
ated learning architecture, requiring data providers to only communicate once
with a central server. However, this methodology encounters its own set of chal-
lenges, particularly with computational efficiency and scalability. It especially
demonstrates limitations in processing high-dimensional data, a common char-
acteristic in complex datasets such as medical images.
In this work, we present an alternative to current randomized encoding meth-
ods for kernel computation in machine learning. We propose a one-shot algo-
rithm, hence bypassing ESCAPED’s communication overheads, while scaling
better than FLAKE to accommodate higher dimensional datasets.
3 Methodology
In this section, we delve into the methodology of our approach, focusing on
private kernel computation in a distributed environment. First, we detail the
adversarial architecture we operate in. In our architecture, for simplicity, we
consider participants Alice, Bob, and Charlie, along with a central server or-
chestrating the training of a machine learning model, as described in Figure 1.
However, this can be extended to any number of participants. We operate under
the assumption of semi-honest participants and a non-colluding central server.
A semi-honest party follows the protocol correctly but may attempt to infer
additional information. This is in line with existing state-of-the-art [32,20].
Bob
Sending
encoded data 
to central 
server
Charlie
Alice
Seed Sharing
𝐵𝑜𝑏′𝑠 𝑑𝑎𝑡𝑎 𝐶ℎ𝑎𝑟𝑙𝑖𝑒′𝑠 𝑑𝑎𝑡𝑎
Projection 
of sensitive 
data into 
private space 
𝐴𝑙𝑖𝑐𝑒′𝑠 𝑑𝑎𝑡𝑎
Kernel Computation &
Machine Learning
Inference, Update & 
Deletion Queries
Fig. 1. Overview of OKRA.
Our method must satisfy four key requirements, with privacy being the
first: Neither the central server, nor the corrupted participants can learn a non-

Private, Efficient and Scalable Kernel Learning for Medical Image Analysis 5
corrupt participant’s data, and the image sizes remain concealed from the server.
Second, correctness is crucial, with the model’s accuracy needing to align that
of a centrally trained model. Third,efficiency is important, as communication
costs and execution times should be practical even when input data scales up.
Finally, data adaptability is essential, allowing the model to accommodate
new data and participants with minimal overhead.
We will focus on four of the most widely used kernel functions: Linear, Gaus-
sian, Polynomial, and Rational Quadratic kernels. We begin by briefly defining
them.
3.1 Preliminaries
Kernel functions project the data into a Hilbert space using a feature map,
and compute the similarity between the data points in this space. The trick
here lies in the ability to compute this similarity without explicitly mapping
the data - a consequence of Mercer’s theorem, which provides necessary and
sufficient conditions for a function from an input space to be a ’kernel’, ensuring
the mapped data resides in a Hilbert space. Below are four widely used kernels
of interest: Linear Kernel (Klin) [11], Gaussian Kernel (KRBF) [6], Polynomial
Kernel (Kpoly) [27], and Rational Quadratic Kernel (KRQ) [33] -
Klin(x, y) =xyT , K RBF (x, y) =γ2 exp

− ∥x − y∥2
2l2

,
Kpoly(x, y) = (1 +xyT )d, K RQ(x, y) =γ2

1 +∥x − y∥2
2αl2
−α
.
Here, γ is the amplitude,l the length-scale, d the degree of the polynomial,
and α the scale mixture. We now define orthonormal k-frames, that are central
to our study.
Definition 1. Orthonormal k-frame [10]
A k-frame is an ordered set ofk linearly independent vectors in a vector space of
dimension n, with k ≤ n. An ordered set ofk linearly independent orthonormal
vectors is called anOrthonormal k-frame.
3.2 The OKRA Methodology
Data Preprocessing Prior to delving into our methodology, we now detail
the preprocessing steps for medical imaging datasets. Each dataset comprisesn
medical images, formatted into a four dimensional array of sizen × h × w × c,
where histheheight, w thewidth,and cthenumberofcolorchannels.Weflatten
each image into a 1D array, so that the dataset has the sizen × (hwc := f ).
Participants Alice, Bob, and Charlie possess preprocessed data matricesA, B,
and C of size nA × f, nB × f, and nC × f respectively. While nA, nB, and
nC may differ due to variable data availability among participants, we require
all participants contribute more than one image. The participants share a seed

6 A. Hannemann and A. Swaminathan et al.
using any robust Public Key Infrastructure (PKI) for secure communication.
We assume a trusted third party for fair public key distribution, in line with
standard privacy-preserving federated learning practices.
Seed Generation A robust Public Key Infrastructure (PKI) ensures every
participant possesses the public signing keys of all others. At the onset of the
protocol, a participant is arbitrarily designated as the leader, responsible for
the generation of a random seed. A secure seed is shared with participants
using public-key encryption and verified with digital signatures. We assume a
trusted third party for fair public key distribution, in line with standard privacy-
preserving federated learning practices [5,36].
Randomized Encoding The participants Alice (A), Bob (B) and Charlie
(C) with their shared seeds generate their own sets ofj orthonormal k-frames
(AO1, . . . ,AOj), (BO1, . . . ,BOj), and(CO1, . . . ,COj) respectively, using the seed
such that
P Oi = [P v1
i
T
. . .P vki
i
T
],
for P ∈ {A, B, C}. Further, for anyp ≤ j and P, Q ∈ {A, B, C}, it holds that
 
P O†
p

(QOp) =I,
where † denotes the conjugate transpose. Each P vl
i is an element of a cor-
responding vector space Vi defined over C such that ki ≤ dim(Vi). Further,
V1 ⊕ . . .⊕ Vj = V, dim(V ) =f + k, and k1 + . . .+ kj = f. Then we defineP Γ
to be the direct sum
P Γ = P O1 ⊕ · · · ⊕P Oj.
To enhance privacy, a random permutation matrixσ ∈ Sf is generated using
the shared seed by all three participants. HereSf denotes the symmetric group
of degree f. They then permute the rows of their matrices AΓ, BΓ, and CΓ
according to this permutation, and subsequently, encode their data to derive
A′ = A(AΓ ◦ σ)† ∈ CnA×(f +k), B′ = B(BΓ ◦ σ)† ∈ CnA×(f +k), and C ′ =
C(CΓ ◦ σ)† ∈ CnC×(f +k).
Alice, Bob, and Charlie sendA′, B′, and C ′ to the central server. LetAi de-
note theith row of matrixA - an image in our setting. We propose the following.
Theorem 1. Given A′, B′ and C ′, the central server can correctly compute the
Linear, Gaussian, the Polynomial and the Rational Quadratic Kernels for the
distributed input data.
Proof. Without loss of generality, let us consider the kernels to be computed
between Alice and Bob. Let us denote an image from Alice asa = Ai, and Bob
as b = Bj. Then representing the encoded images asa′ = A′
i and b′ = B′
j, we
propose that the functions to be computed by the central server are as follows.
K †
lin(a′, b′) = [(A′
i)(B′
j)†], K †
RBF (a′, b′) = exp
 
− γdij(A′, B′)

,
K †
poly(a′, b′) =
 
1 + [(A′
i)(B′
j)†]
d
, K †
RQ(a′, b′) =γ2

1 +dij(A′, B′)
2αl2
−α
,

Private, Efficient and Scalable Kernel Learning for Medical Image Analysis 7
where
dij(A′, B′) :=
 
[(A′
i)(A′
i)†] + [(B′
j)(B′
j)†] − [(A′
i)(B′
j)†] − [(B′
j)(A′
i)†]

.
To show that these are well defined kernels, we prove the correctness of the
computed functions. Without loss of generality forP, Q∈ {A, B} and any p, q-
[(P ′
p)(Q′
q)†] =

(P ′)
 
QΓ σ(Qq)†
p =
"
P σ†
 qM
k=1
P O†
kQOk
!
σQq
#
p
= [PpQq] .
Hence, it follows that
[(A′
i)(B′
j)†] =abT , [(B′
j)(A′
i)†] =baT ,
[(A′
i)(A′
i)†] =aaT , [(B′
j)(B′
j)†] =bbT ,
K †
lin(a′, b′) =Klin(a, b), K †
RBF (a′, b′) =KRBF (a, b),
K †
poly(a′, b′) =Kpoly(a, b), K †
RQ(a′, b′) =KRQ(a, b).
This shows the correctness of the computed functions, hence theoretically
satisfying ourCorrectness requirement. Further, to show that these functions
are well defined kernels, we note that the map Γ : Rf → Cf +k defined by
P Γ (v) =v′ for v ∈ Rf and P ∈ {A, B, C} is a bijection, and sinceKlin, KRBF ,
Kpoly and KRQ are well defined kernels, so are K †
lin = Klin ◦ (Γ −1 × Γ −1),
K †
RBF = KRBF ◦ (Γ −1 × Γ −1), K†
poly = Kpoly ◦ (Γ −1 × Γ −1), and K †
RQ =
KRQ ◦ (Γ −1 × Γ −1) on the range ofΓ × Γ.
Cf +k × Cf +k
Rf × Rf R
H × H
Γ ×Γ
ϕ×ϕ
(Γ −1◦ϕ)×(Γ −1◦ϕ)
⟨·,·⟩
K
K†
Hence we have the above commutative diagram.
3.3 Data Adaptability
In our methodology, Alice, Bob, and Charlie contribute datasetsA, B, and C.
Introducing additional dataX from Charlie or another participant is seamless.
The shared seed is used to generateX ′ for further kernel computations with
the existing data. Only specific kernel portions are updated, saving computa-
tional resources. When data changes dynamically, OKRA creates new masks,
denoted by Γt for training iteration t, ensuring privacy for each party’s data
alterations. If a participant withdraws data, the corresponding contribution is
removed, complying with data protection standards such as the GDPR.

8 A. Hannemann and A. Swaminathan et al.
4 Privacy Analysis
As stated earlier, OKRA operates under the environment consisting of a proper
subset of semi-honest participants, and/or a non-colluding semi-honest central
server. For this purpose, we will show that it guarantees security in both settings.
It is essential to highlight that our privacy model excludes certain extreme
adversarial conditions. We exclude data distributions where the number of fea-
tures or the training data of one or more input parties can be guessed, and
protocols with only one input party.
Theorem 2. The proposed methodology is secure against a semi-honest adver-
sary who corrupts the central server.
Proof. A semi-honest central server is only the receiver of the encoded data
from the input parties, and follows the protocol as intended. Without loss of
generality, let there be two input parties Alice and Bob with input dataA ∈
RnA×f and B ∈ RnB×f, respectively, wherenP is the number of samples with the
corresponding party P ∈ {A, B} and f is the number of features in each image.
The semi-honest function party receives the projected data from Alice and Bob.
These consist of A′ = Aγ† ∈ CnA×(f +k) and B′ = Bγ † ∈ CnB×(f +k) where
k >0. Then, it computes the kernel functions mentioned above in Theorem 1.
The data to which the function party has access then includes
(a) A′ and analogously,B′,
(b) ABT = (BAT )T, AAT and analogously BB T.
Regarding (a), it is evident thatA′ does not reveal the number of features ofA.
We now show thatA′ is not produced by a unique pairA and AΓ ◦ σ.
Given a unitary matrix U ∈ Cf ×f with f > 1, for ˜A = AU and A ˜Γ =
Γ ◦ σ ◦ U, we haveA′ = A(AΓ ◦ σ)† = ˜AA ˜Γ †. In the context of reconstruction
attacks using analogous data, consider a sample datasetˆA that is drawn from
a distribution similar to A. In the context of reconstructingA, the goal is to
find a transformation matrixR such that A′R = ˆA approximates A. However,
since ˆA and A do not exist within the same feature space, this leads to loss of
information, rendering the approximation ineffective. Further, sinceΓ consists
of orthogonal vectors, the inability to approximateA can also be attributed to
the unbalanced orthogonal procrustes problem which is unsolved [16].
Regarding (b), we adopt the proof from [32]. The matrices that produce
these symmetric matrices are not unique, since for any unitary matrix U ∈
C(f +k)×(f +k) where f >1, labeling ˜A = A′U and ˜B = B′U, we have
˜A ˜AT = AAT , ˜B ˜BT = BB T , ˜A ˜BT = ABT .
Similar to the prior argument, these results can also be derived from data in a
different feature space. As a result, the function party is limited to learning only
the singular values and vectors of the matrices. This means it can deriveU and S
from the singular value decompositionA = U SVT by eigen-decomposing AAT.
Yet, this information is inadequate to deduceA since V is unknown. Thus, the
functionpartydoesnotlearn(i) the input data or (ii) the number ofthe features.

Private, Efficient and Scalable Kernel Learning for Medical Image Analysis 9
Theorem 3. The proposed methodology is secure against a proper subset of
semi-honest participants.
Proof. Since the proposed methodology follows one-shot federated learning with
no communication back from the central server, the uni-directional flow of data
prohibits the corrupt participants from learning anything about the data of the
non-corrupt participants.
Therefore, we’ve shown that the data of non-corrupt participants can not be
learned by corrupt semi-honest participants, and that the central server doesn’t
learn the image sizes, satisfying ourPrivacy requirement.
5 Experiments
Experiments were conducted on an AMD 7713 at 2.0GHz with one CPU core
and 16 GB of RAM, simulating hospitals collaboratively performing kernel-
learningwithlimitedresources.Communicationsettingsincludedabandwidthof
1.25MBps, an average latency of0.1s, and a packet loss of2%. Unless stated oth-
erwise, OKRA was tested with three participants. Each participant operated as
an independent process using TCP connections. Data encoding and transmission
to the central server were done via multiple threads. The server performed kernel
functions on aggregated data for machine learning model training. Experiments
were deemed successful if OKRA’s accuracy matched non-private classification
methods and surpassed the run-times of state-of-the-art randomized encoding
algorithms, ESCAPED [32] and FLAKE [20].
5.1 Datasets
To demonstrate OKRA’s applicability, we experimented with two clinical image
datasets with different label types and distributions. The first dataset consists
of preprocessed MRI images capturing various stages of Alzheimer’s disease [22].
The second dataset features augmented images of white blood cells, representing
four distinct cell types [29]. For run-time analysis, we used synthetic datasets,
essential for benchmarking without real-world data irregularities. The generated
data is balanced, with multi-class clusters drawn from a multivariate normal
distribution (mean 0, variance 1 for each attribute). We generated400 samples
per participant with1000 features.
5.2 Correctness of the Model
Before beginning the run-time experiments, we aimed to validate OKRA’s cor-
rectness on kernel learning methods. We conducted classification using SVM and
dimensionality reduction with Kernel-PCA. Each experiment was run 10 times,
testing various combinations of datasets, methods, and kernels (Gaussian, Poly-
nomial, and Linear). Seeds were used for deterministic behavior and reproducible
results.

10 A. Hannemann and A. Swaminathan et al.
For the classification task, OKRA-SVM was tested against a Naive SVM.
Both implementations shared identical hyperparametersC ∈ {2−4, ...,210} (mis-
classification penalty) andp ∈ {1, ...,5} (degree), optimized using Grid Search.
Both were trained with a 5-fold cross-validation. For this implementation, we
used Sequential Minimal Optimization (libsvm) provided by scikit-learn [35].
We applied Macro Averaging when the datasets had an unbalanced distribution
of classes. Correspondingly, we have evaluated the balanced datasets with Micro
Averaging. Table 5.2 shows that OKRA-SVM and the naive classifier produce
the same F1 and ROC AUC scores.
T able 1. Performance metrics for
OKRA-PCA
Dataset Kernel OKRA
MSE R2
Alzheimer’s
Disease Polynomial 0.0 1.0
Blood Cell Gaussian 0.0 1.0
For the dimensionality reduction, we com-
pared a naive Kernel-PCA and OKRA-PCA.
A kernel is computed, followed by eigenvalue
decomposition to sort eigenvalues and eigen-
vectors by magnitude. The topn eigenvectors
are then chosen to transform the data into the
newprincipalcomponentspace.Toassessutil-
ity, the principal components of both Kernel-
PCA and OKRA-PCA, utilizing the same ker-
nel, were compared by computing the Mean
Squared Error (MSE) and R-squared (R2).
Dataset
(Samples×Features) Label Type Kernel Naive OKRA
F1 ROC AUC F1 ROC AUC
Alzheimer’s Disease
(6400×256· 256)
Binary Gaussian 0.91±0.03 0.97±0.01 0.91±0.03 0.97±0.01
Multi-class Gaussian 0.97±0.04 1.00±0.00 0.97±0.04 1.00±0.00
Blood Cell
(12500×100· 100· 3) Multi-class Gaussian 0.88±0.01 0.94±0.01 0.88±0.01 0.94±0.01
Synthetic
(200−51200×12800) Multi-class Linear 0.89±0.03 0.95±0.02 0.89±0.03 0.95±0.02
This provides a quantitative comparison of the two PCA methods in terms of
their ability to capture the data’s variance and structure. Table 1 indicates that
both OKRA-PCA and naive PCA are highly consistent and produce identical
results, explaining the same patterns in the data. As expected, the encoding has
no influence on the results. Hence we experimentally satisfy theCorrectness
requirement.
5.3 Performance Analysis
To ensure OKRA’s computational overhead is manageable, especially with high-
dimensional datasets like images, we compared its run-time with FLAKE and
ESCAPED. We focused on two run-time types:Encoding time, the overhead
of encoding data using OKRA for an individual participant, andTotal time,
which includes communication from when the server initiates connections to
the completion of the kernel function computation. Our analysis examined the
impact of varying the number of participants and image sizes. i

Private, Efficient and Scalable Kernel Learning for Medical Image Analysis 11
Scaling up the Number of Participants Evaluating our method’s adaptability
across multiple participants is crucial. Figure 2 shows the cumulative time re-
quired for data encoding, transmission, and linear kernel function computation.
Each participant encodes a dataset of 400 samples with 1000 features. OKRA
performs exceptionally well: with 10 participants, the execution takes only 16
seconds on average.
3 4 5 6 7 8 9 10
0
20
40
60
No. of Participants
Time (Seconds)
ESCAPED FLAKE OKRA
Fig. 2. Runtime comparison with increasing participants.
Scaling up the Image SizeMedical image data, essential for accurate diagnoses
and treatment, is typically captured at high resolutions. However, for preprocess-
ing, these images are often scaled down for memory and computational efficiency,
with rescaled sizes ranging from32×32up to256×256. To assess whether OKRA
can encode preprocessed medical images without burdening the data holder, we
experimented with increasing image sizes for one participant with 400 images
(refer to Fig. 3). The results demonstrate that OKRA is applicable to medi-
cal imaging, whereas state-of-the-art methods are not. We, therefore, meet both
requirements Data Adaptabilityand Efficiency.
5.4 Discussion
Randomized encoding methods, used for privacy-preserving kernel learning, of-
fer the advantage of computational efficiency while maintaining model accuracy.
In the field of randomized encoding methods, our proposed solution, OKRA,
demonstrates significant advantages. It consistently outperforms both FLAKE
and ESCAPED without compromising utility. Notably, OKRA minimizes the
need for extended communication rounds and supports data adaptability, issues
primarily encountered with ESCAPED. Additionally, OKRA achieves more effi-
cient data encoding than FLAKE and can handle larger image sizes. With these
strengths, OKRA emerges as a robust and efficient option within the domain of
randomized encoding techniques for image data.

12 A. Hannemann and A. Swaminathan et al.
128 512 2048 8192 32768 131072 524288
10−2
100
102
Image Size (px× px)
Time (Seconds)
FLAKE OKRA ESCAPED
Fig. 3. Encoding times against image sizes.
In subsequent work, we aim to explore the challenges associated with the
colluding central server scenario. Further, we intend to address malicious par-
ticipant behavior, where encoded data is altered to cause inaccuracies in the
server’s results. Additionally, we plan to explore the applicability of OKRA to
other kernel methods, given its promising potential.
6 Conclusion
Privacy preservation for the analysis of distributed medical images remains a
critical challenge. While randomized encoding offers a promising avenue, exist-
ing methodologies often grapple with the trade-off between accuracy and effi-
ciency. Addressing this gap with regards to kernel functions applied to high-
dimensional data, we introduced OKRA, a novel algorithm operating within a
one-shot federated learning paradigm. OKRA not only privately computes exact
kernel functions but also ensures that kernel-based machine learning algorithms
are trained efficiently. Empirical evaluations further validate the superiority of
OKRA, demonstrating its potential to achieve accuracy levels comparable to
centralized machine learning models while minimizing computational burdens.
As the landscape of machine learning continues to evolve, OKRA’s robustness
and efficiency position it as a pivotal tool in privacy-preserving endeavors.
Acknowledgments.This study is supported by the German Federal Ministry of Re-
search and Education (BMBF), under project number 01ZZ2010.
References
1. Adnan, M., Kalra, S., Cresswell, J.C., Taylor, G.W., Tizhoosh, H.R.: Federated
learninganddifferentialprivacyformedicalimageanalysis.Scientificreports 12(1),
1–10 (2022)
2. Al-Jaroodi, J., Mohamed, N., Abukhousa, E.: Health 4.0: on the way to realizing
the healthcare of the future. Ieee Access8, 211189–211210 (2020)

Private, Efficient and Scalable Kernel Learning for Medical Image Analysis 13
3. Applebaum, B., Ishai, Y., Kushilevitz, E.: Computationally private randomiz-
ing polynomials and their applications. computational complexity15(2), 115–162
(2006)
4. Bagdasaryan, E., Poursaeed, O., Shmatikov, V.: Differential privacy has disparate
impact on model accuracy. Advances in neural information processing systems32
(2019)
5. Bonawitz, K., Ivanov, V., Kreuter, B., Marcedone, A., McMahan, H.B., Patel, S.,
Ramage,D., Segal,A., Seth,K.: Practical secureaggregationfor privacy-preserving
machine learning. In: proceedings of the 2017 ACM SIGSAC Conference on Com-
puter and Communications Security. pp. 1175–1191 (2017)
6. Boser, B.E., Guyon, I.M., Vapnik, V.N.: A training algorithm for optimal margin
classifiers. In: Proceedings of the fifth annual workshop on Computational learning
theory. pp. 144–152 (1992)
7. Chen,H.,Ünal,A.B.,Akgün,M.,Pfeifer,N.:Privacy-preservingsvmonoutsourced
genomic data via secure multi-party computation. In: Proceedings of the Sixth
International Workshop on Security and Privacy Analytics. pp. 61–69 (2020)
8. Chen, K., Liu, L.: Geometric data perturbation for privacy preserving outsourced
data mining. Knowledge and information systems29, 657–695 (2011)
9. Chen, K., Sun, G., Liu, L.: Towards attack-resilient geometric data perturbation.
In: proceedings of the 2007 SIAM international conference on Data mining. pp.
78–89. SIAM (2007)
10. Christensen, O., et al.: An introduction to frames and Riesz bases, vol. 7. Springer
(2003)
11. Cortes, C., Vapnik, V.: Support-vector networks. Machine learning20, 273–297
(1995)
12. Costache, A., Smart, N.P.: Which ring based somewhat homomorphic encryp-
tion scheme is best? In: Topics in Cryptology-CT-RSA 2016: The Cryptographers’
Track at the RSA Conference 2016, San Francisco, CA, USA, February 29-March
4, 2016, Proceedings. pp. 325–340. Springer (2016)
13. Dou, B., Zhu, Z., Merkurjev, E., Ke, L., Chen, L., Jiang, J., Zhu, Y., Liu, J., Zhang,
B., Wei, G.W.: Machine learning methods for small data challenges in molecular
science. Chemical Reviews123(13), 8736–8780 (2023)
14. El Emam, K., Jonker, E., Arbuckle, L., Malin, B.: A systematic review of re-
identification attacks on health data. PloS one6(12), e28071 (2011)
15. Gentry, C.: Fully homomorphic encryption using ideal lattices. In: Proceedings
of the forty-first annual ACM symposium on Theory of computing. pp. 169–178
(2009)
16. Gower, J.C., Dijksterhuis, G.B.: Procrustes problems, vol. 30. OUP Oxford (2004)
17. Griebel, L., Prokosch, H.U., Köpcke, F., Toddenroth, D., Christoph, J., Leb, I.,
Engel, I., Sedlmayr, M.: A scoping review of cloud computing in healthcare. BMC
medical informatics and decision making15(1), 1–16 (2015)
18. Guha, N., Talwalkar, A., Smith, V.: One-shot federated learning. arXiv preprint
arXiv:1902.11175 (2019)
19. Hannemann, A., Friedl, B., Buchmann, E.: Differentially private multi-label learn-
ing is harder than you’d think. In: 2024 IEEE European Symposium on Security
and Privacy Workshops (EuroS&PW). pp. 40–47. IEEE (2024)
20. Hannemann, A., Ünal, A.B., Swaminathan, A., Buchmann, E., Akgün, M.: A
privacy-preserving framework for collaborative machine learning with kernel meth-
ods. In: 2023 5th IEEE International Conference on Trust, Privacy and Security
in Intelligent Systems and Applications (TPS-ISA). pp. 82–90. IEEE (2023)

14 A. Hannemann and A. Swaminathan et al.
21. Hasan, B.M.S., Abdulazeez, A.M.: A review of principal component analysis algo-
rithm for dimensionality reduction. Journal of Soft Computing and Data Mining
2(1), 20–30 (2021)
22. LaMontagne, P.J., Benzinger, T.L., Morris, J.C., Keefe, S., Hornbeck, R., Xiong,
C., Grant, E., Hassenstab, J., Moulder, K., Vlassenko, A.G., et al.: Oasis-3: longitu-
dinal neuroimaging, clinical, and cognitive dataset for normal aging and alzheimer
disease. MedRxiv pp. 2019–12 (2019)
23. Lin, K.P., Chang, Y.W., Chen, M.S.: Secure support vector machines outsourcing
with random linear transformation. Knowledge and Information Systems44, 147–
176 (2015)
24. McMahan, B., Moore, E., Ramage, D., Hampson, S., y Arcas, B.A.:
Communication-efficient learning of deep networks from decentralized data. In:
Artificial intelligence and statistics. pp. 1273–1282. PMLR (2017)
25. Mothukuri, V., Parizi, R.M., Pouriyeh, S., Huang, Y., Dehghantanha, A., Srivas-
tava, G.: A survey on security and privacy of federated learning. Future Generation
Computer Systems 115, 619–640 (2021)
26. Mugunthan, V., Polychroniadou, A., Byrd, D., Balch, T.H.: Smpai: Secure multi-
party computation for federated learning. In: Proceedings of the NeurIPS 2019
Workshop on Robust AI in Financial Services (2019)
27. Schölkopf, B., Smola, A.J.: Learning with kernels: support vector machines, regu-
larization, optimization, and beyond. MIT press (2002)
28. Seo, H., Badiei Khuzani, M., Vasudevan, V., Huang, C., Ren, H., Xiao, R., Jia,
X., Xing, L.: Machine learning techniques for biomedical image segmentation: an
overview of technical aspects and introduction to state-of-art applications. Medical
physics 47(5), e148–e167 (2020)
29. Shenggan: Bccd dataset. https://github.com/Shenggan/BCCD_Dataset (2017),
accessed on 27.07.2023
30. Swaminathan, A., Hannemann, A., Ünal, A.B., Pfeifer, N., Akgün, M.: Pp-gwas:
Privacy preserving multi-site genome-wide association studies. arXiv preprint
arXiv:2410.08122 (2024)
31. Ünal, A.B., Akgün, M., Pfeifer, N.: A framework with randomized encoding for a
fast privacy preserving calculation of non-linear kernels for machine learning appli-
cations in precision medicine. In: Cryptology and Network Security: 18th Interna-
tional Conference, CANS 2019, Fuzhou, China, October 25–27, 2019, Proceedings
18. pp. 493–511. Springer (2019)
32. Ünal, A.B., Akgün, M., Pfeifer, N.: Escaped: Efficient secure and private dot
product framework for kernel-based machine learning algorithms with applications
in healthcare. In: Proceedings of the AAAI Conference on Artificial Intelligence.
vol. 35, pp. 9988–9996 (2021)
33. Williams, C., Rasmussen, C.: Gaussian processes for regression. Advances in neural
information processing systems8 (1995)
34. Yao, A.C.: Protocols for secure computations. In: 23rd annual symposium on foun-
dations of computer science (sfcs 1982). pp. 160–164. IEEE (1982)
35. Zeng, Z.Q., Yu, H.B., Xu, H.R., Xie, Y.Q., Gao, J.: Fast training support vector
machines using parallel sequential minimal optimization. In: 2008 3rd international
conference on intelligent system and knowledge engineering. vol. 1, pp. 997–1001.
IEEE (2008)
36. Zhang, C., Li, S., Xia, J., Wang, W., Yan, F., Liu, Y.: Batchcrypt: Efficient homo-
morphic encryption for cross-silo federated learning. In: Proceedings of the 2020
USENIX Annual Technical Conference (USENIX ATC 2020) (2020)