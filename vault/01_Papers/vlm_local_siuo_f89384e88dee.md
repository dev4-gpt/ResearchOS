---
title: "siuo"
source_type: "original_local_pdf"
source_path: "/Users/aryamandev/Developer/blissful-bose/presentation/paper_pdfs/siuo.pdf"
source_sha256: "f89384e88deee31656339a6dbf56beab17d4053082de2437b848cdde2886b316"
project: "vlm-safety"
full_pdf_ingested: "True"
page_count: "15"
pages_with_extracted_text: "15"
bibliographic_metadata_verified: "False"
visual_review_completed: "False"
---
arXiv:2410.01275v2  [math.CA]  17 Feb 2025
TOPOLOGICAL ERD ˝OS SIMILARITY CONJECTURE AND
STRONG MEASURE ZERO SETS
YEONWOOK JUNG AND CHUN-KIT LAI
Abstract. We solve a topological variant of the Erd˝ os similarity conjecture posed
by Gallagher, Lai, and Weber. Particularly, we prove that the existe nce of an
uncountable subset of the real line that is universal in the family of all dense Gδ sets
is independent of the usual axioms of set theory. Such sets are sh own to correspond
to strong measure zero sets, which were ﬁrst introduced by Bore l. Applying the
duality principle between measure and category to this result, we derive a conjecture
that is strong enough to prove the Erd˝ os similarity conjecture for perfect sets.
1. Introduction
A subset X of R is said to be universal in a family F of subsets of R if every
F ∈ F contains an aﬃne copy of X, i.e., λX +t ⊂ F for some λ ∈ R \ {0} and
for some t ∈ R. A subset X of R is said to be measure universal if it is universal
in the family of all Lebesgue measurable subsets of R that have positive Lebesgue
measure. It is a consequence of the Lebesgue density theorem th at ﬁnite sets are
universal [ 32]. Based on this observation, Erd˝ os conjectured that there is no inﬁnite
measure universal set, referred to as the Erd˝ os similarity conje cture [ 8].
Conjecture 1.1 (Erd˝ os). No inﬁnite subset of the real line is measure universal.
To prove the Erd˝ os similarity conjecture, it suﬃces to show that a ll sequences
that monotonically decreases and converges to zero are not unive rsal. Among such
sequences, sublacunary sequences {an}, i.e., those that satisfy lim n→∞
an+1
an
= 1, are
known to be not measure universal [ 6, 10], but exponentially decaying sequences,
such as {2−n}, remain unanswered. Also, sumsets of the form {an} + {bn} + {cn} or
{2−nα
} + {2−nα
} are not measure universal [ 4, 20]. A comprehensive survey on the
Erd˝ os similarity conjecture containing results published before year 2000 can be found
in [ 33]. A review on some of the recent progress on the Erd˝ os similarity co njecture
can be found in [ 18].
Despite these results, arbitrary countable sets still remain elusive in terms of mea-
sure universality. In particular, the Erd˝ os similarity conjecture r emains open for
arbitrary uncountable sets, and even for perfect sets.
2010 Mathematics Subject Classiﬁcation. Primary .
1

2 YEONWOOK JUNG AND CHUN-KIT LAI
In part of the eﬀort to further understand the Erd˝ os similarity c onjecture, Gal-
lagher, Lai, and Weber recently considered a topological variant of the Erd˝ os simi-
larity conjecture by deﬁning topological universality as follows [ 13]. A subset X of
R is said to be topologically universal if it is universal in the family of all dense
Gδ subsets of R. They observed that countable sets are topologically universal by
the Baire category theorem and proved that perfect sets are no t topologically univer-
sal. In particular, they completed the analogy to the Erd˝ os similarit y conjecture by
stating the following conjecture.
Conjecture 1.2 (Gallagher-Lai-Weber). No uncountable subset of the real line is
topologically universal.
In this paper, we give a complete solution to Conjecture
1.2 on R and more generally
on locally compact Polish groups. We then discuss its implication to the o riginal Erd˝ os
similarity conjecture. The main results and the outline of this paper a re given below.
In Section 2, we prove that Conjecture 1.2 is independent of the standard axioms of
set theory, namely, Zermelo-Fraenkel axioms of set theory with a xiom of choice ( ZFC).
We achieve this by proving that the topologically universal sets are precisely the strong
measure zero sets , which is deﬁned as the following. A subset X of the real line is
a strong measure zero set if for every sequence {ǫn}∞
n=1 of positive real numbers,
there exists a sequence of intervals {In}∞
n=1 such that X ⊂ ∪ ∞
n=1In and |In| < ǫn.
Note that all countable sets are strong measure zero sets. Borel conjecture is the
statement that all strong measure zero sets are countable [
7]. It is known that the
Borel conjecture is independent of ZFC: Sierpi´ nski [31] proved the consistency of the
negation of the Borel conjecture, and Laver [ 23] proved the consistency of the Borel
conjecture. This concludes that Conjecture 1.2 is independent of ZFC.
The fact that Conjecture 1.2 is independent of ZFC readily generalizes to a more
general space of locally compact Polish groups. In particular, this in cludes Rd as
a special case. Similar to the case of the real line, we prove that the existence
of uncountable topologically universal set in any locally compact Polish group is
independent of ZFC. This is proved in Section 3. Although the result for the real line
can be deduced from the result for locally compact Polish groups, we still choose to
present the proof for the real line since the proof is clearer withou t the additional
deﬁnitions and the caveats for working in locally compact Polish group s.
In Section 4, our resolution of this topological variant of the Erd˝ os similarity co n-
jecture is connected to the original Erd˝ os similarity conjecture in the following way.
Under the principle of duality between measure and category, we ob tain the following
conjecture as a dual statement of our main result in section 2: a su bset of the real
line is universal in the family of all sets of full measure if and only if it is a s trongly
meager set. Since perfect sets are not strongly meager [ 9], if this conjecture is true,
then perfect sets are not universal in sets of full measure, and t hus, not measure

TOPOLOGICAL ERD ˝OS SIMILARITY CONJECTURE AND SMZ SETS 3
universal. This would establish a stronger version of the Erd˝ os simila rity conjecture
for perfect sets.
1.1. Notation and basic deﬁnitions. Unless stated otherwise, we work in the
Zermelo–Fraenkel set theory with axiom of choice ( ZFC). For subsets A,B of a group,
A +B = {a +b :a ∈A,b ∈B} denotes the algebraic sum or the Minkowski sum of
A and B. If X is a subset of a vector space, then λX = {λx : x ∈ X}, where λ is
a scalar, denotes the scaling of X by λ. In a topological space, a meager set is a
countable union of nowhere dense sets. A nowhere dense set is a set whose closure
has empty interior. A set is comeager if its complement is meager. A topological
space is called a Baire space if every meager set has no interior, or equivalently,
every comeager set is dense. A σ-ideal is a collection of sets that contains the empty
set and is closed under taking subsets and countable unions.
2. Topologically universal sets in R
In this section, we classify topologically universal sets in R and answer the Conjec-
ture
1.2.
Lemma 2.1. In a Baire space, every dense Gδ set contains a comeager set and every
comeager set contains a dense Gδ.
Proof. LetX be a Baire space. Let G be a dense Gδ subset of X. Then, G = ∩∞
n=1Gn
for some open subsets Gn of X, where each Gn is dense since cl( Gn) ⊃ cl(G) = X.
Note that X
∖ G = X ∖ (∩∞
n=1Gn) = ∪∞
n=1(X
∖ Gn), where X ∖ Gn is nowhere dense
since
(
cl(X ∖ Gn)
) ◦
= (X ∖ Gn)◦ = X ∖ cl(Gn) = ∅. Hence, X ∖ G is a meager set
and G is a comeager set. Thus, G contains a comeager set, namely, G itself.
Next, let H be a comeager subset of X. Then, H =X∖ M for some meager subset
M ofX andM = ∪∞
n=1Nn, where each Nn is a nowhere dense subset of X. Since each
cl(Nn) is also a nowhere dense subset of X, ∪∞
n=1cl(Nn) is a meager Fσ set, implying
that X
∖ ∪∞
n=1cl(Nn) is a comeager Gδ set that is a subset of H. Since X is a Baire
space and comeager sets are dense in Baire spaces, H contains a dense Gδ set. □
Lemma 2.2. A subset X of R is topologically universal if and only if X is universal
in the family of all comeager sets.
Proof. Let X be a topologically universal subset of R and H be a comeager subset
of R. By Lemma
2.1, there exists a dense Gδ set G such that G ⊂ H and since X
is topologically universal, there is an aﬃne copy λX +t, for some λ ̸= 0 and t ∈ R,
of X, such that λX +t ⊂ G. Thus, λX +t ⊂ H and X is universal in comeager
sets. The other direction is obtained by the same proof upon excha nging comeager
sets and Gδ sets. □

4 YEONWOOK JUNG AND CHUN-KIT LAI
In order to make connection between topologically universal sets a nd strong mea-
sure zero sets in R, we need the following key theorem by Galvin, Mycielski, and
Solovay [14] (announced without proof). For a proof, see [ 1] and [ 15].
Theorem A (Galvin-Mycielski-Solovay). A subset X of R is a strong measure zero
set if and only if for every meager set M in R, X +M ̸= R.
We notice that topological universality can also be phrased as a sum s et problem
similar to the Galvin-Mycielski-Solovay theorem (Theorem A).
Lemma 2.3. A subset X of R is topologically universal if and only if for every meager
set M in R, there exists λ ∈ R∖ {0} such that X +λM ̸= R.
Proof. We ﬁrst prove the only if. Suppose X is topologically universal subset of R.
Then, by Lemma 2.2, for every meager set M in R, there exists λ′ ∈ R \ {0} and
t ∈ R such that λ′X +t ⊂ M c, i.e., ( λ′X +t) ∩M = ∅. This implies that for all
x ∈ X and y ∈ M, λ′x +t ̸= y, i.e., x − 1
λ′y ̸= − t
λ′ . Hence, − t
λ′ ̸∈X − 1
λ′M, i.e.,
X − 1
λM ̸= R. Taking λ = − 1
λ′ , we have X +λM ̸= R.
To see the if part, let X be a subset of R and suppose that for each meager set N
in R, there exists λ′ ∈ R \ {0} such that X +λ′N ̸= R. Let M be a meager set in
R. Then, there exists a ∈ R such that for all x ∈ X and y ∈ M, x +λ′y ̸= a, i.e.,
1
λ′x − a
λ′ ̸= −y. Thus, by letting λ = 1
λ′ andt = − a
λ′ , we have (λX +t) ∩M = ∅, i.e.,
λX +t ⊂ M c. Therefore, X is universal in comeager subsets of R, and by Lemma
2.2, X is topologically universal. □
Theorem 2.4. A subset of the real line is topologically universal if and on ly if it is
a strong measure zero set.
Proof. We ﬁrst show the if part. Suppose that X is a strong measure zero set. By the
Galvin-Mycielski-Solovay theorem (Theorem
A), X +M ̸= R for all meager sets M
in R. We now take λ = 1 and apply Lemma 2.3 to conclude that X is topologically
universal.
Next, we show the only if part. Let X in R be a topologically universal. Let ( ǫn)n∈N
be a sequence of positive reals. Deﬁne
G =
∞⋂
k=1
∞⋃
n=1
(
qn − ǫn
k,q n + ǫn
k
)
,
where (qn)n∈N is an enumeration of the rational numbers. Since G is a dense Gδ set,
there exists λ ̸= 0 and t ∈ R such that λX +t ⊂G. Let k0 = ⌈ 2
|λ| ⌉. Then,
λX +t ⊂
∞⋃
n=1
(
qn − ǫn
k0
,q n + ǫn
k0
)
,
DenotingIn = 1
λ
(
qn − ǫn
k0
−t,q n + ǫn
k0
−t
)
, we haveX ⊂ ⋃
n∈N
In with |In| = 2ǫn
|λ|k0
≤ǫn.
This proves that X is a strong measure zero set. □

TOPOLOGICAL ERD ˝OS SIMILARITY CONJECTURE AND SMZ SETS 5
Corollary 2.5. Conjecture 1.2 is independent of ZFC.
Proof. This follows from the fact that the Borel conjecture is independen t of ZFC. □
Remark 2.6. In addition to answering Conjecture 1.2, Theorem 2.4 gives a simple
and direct proof of known results about topologically universal set s.
(1) It is now easy to see that countable sets are topologically univer sal. One way to
see this is to recall that countable sets are strong measure zero s ets (almost by
deﬁnition). Another way is to directly use Lemma 2.3, and note that if X ⊂ R
is a countable set and M ⊂ R is a meager set, then X +M is a countable
union of meager sets, which is meager. Since R is a Baire space by the Baire
category theorem, X +M cannot be R, and Lemma 2.3 ﬁnishes the proof.
These oﬀer simple alternative ways to deduce the topological univer sality of
countable sets, which was ﬁrst noted in [ 13].
(2) Perfect sets are not topologically universal since perfect set s are not strong
measure zero sets [ 2, Corollary 8.1.5]. This recovers the previous result [ 13,
Theorem 1.4] (for Rd with d> 1, we prove it in the next section).
(3) Topologically universal sets have zero Hausdorﬀ dimension, sinc e strong mea-
sure zero sets have zero Hausdorﬀ dimension. This recovers a res ult in [ 13,
page 3].
(4) The set of all topologically universal sets form a σ-ideal. This follows from
the fact that strong measure zero sets form a σ-ideal [ 2, Lemma 8.1.2]. The
fact that topologically universal sets form a σ-ideal is a nontrivial statement.
Indeed, it is not hard to see that measure universal sets cannot f orm a σ-ideal
because ﬁnite sets are measure universal while we know some count able sets
are not measure universal.
We elaborate on Remark 2.6 (2). Recall that a set X has the perfect set property
if X contains a perfect subset. It is well known that every Borel set ( more generally,
every analytic set) contains a perfect subset [ 19, Exercise 14.13] (for original refer-
ences, see [ 24] as explained in [ 11, page 3].) Thus, Borel sets are not topologically
universal since they contain perfect sets, which are themselves n ot topologically uni-
versal. Bernstein sets are examples of uncountable subsets of th e real line that do
not have the perfect set property:
Deﬁnition 2.7. A subset B of R is a Bernstein set if for every perfect subset P in
R, B ∩P ̸= ∅ and Bc ∩P ̸= ∅.
Uncountable Bernstein sets can be constructed in ZFC, using the axiom of choice
(see [
19, Example 8.24]). These render the following question in [ 13, page 5] by
Gallagher, Lai, and Weber interesting : Are Bernstein sets topologic ally universal?
We give a negative answer to this question in the next example.
Example 2.8 (Bernstein sets) . Clearly, Bernstein sets are not strong measure zero
sets. This is because strong measure zero sets are Lebesgue mea surable (since strong

6 YEONWOOK JUNG AND CHUN-KIT LAI
measure zero sets have zero Lebesgue measure), but Bernstein sets are not Lebesgue
measurable [
26, Theorem 5.4]. By Theorem 2.4, Bernstein sets are not topologically
universal. This can alternatively be seen from the fact that topolog ically universal
sets have zero Hausdorﬀ dimension, and thus, it has zero Lebesgu e measure implying
that it must be Lebesgue measurable.
3. Generalization to Locally Compact Polish Groups
In this section, we generalize Theorem 2.4 and Corollary 2.5 from R to locally
compact Polish groups. As a special case, we resolve this topologica l variant of the
Erd˝ os similarity conjecture forRd, giving a full answer to [ 13, Conjecture 1.9].
Recall that a Polish space is a separable completely metrizable topolog ical space.
A Polish group ( G, ·) is a topological group that is a Polish space. We denote the
identity element on G by 1G. By Birkhoﬀ–Kakutani theorem, every Polish group
admits a compatible metric d that is left-invariant, but not every Polish group admits
a compatible metric that is simultaneously left-invariant and complete . Every locally
compact Polish group admits a compatible metric that is left-invariant and complete.
We now introduce the aﬃne transformation in locally compact Polish gr oups by
generalizing the deﬁnition of aﬃne transformations in Euclidean spac e. By Haar’s
theorem, for every locally compact Polish group, there is a unique co untably additive
nontrivial Haar measure upto positive multiplicative constant.
Deﬁnition 3.1. Let G be a locally compact Polish group.
(1) The automorphism group of G, denoted by Aut( G), is the collection of
all bijective Haar measurable functions from G to G that preserve the group
operation.
(2) An aﬃne transformation f is a bijection from G to G such that there exists
ϕ ∈ Aut(G) and h ∈ G such that f (g) = h ·ϕ(g) for all g ∈ G.
(3) A subset X of G is topologically universal in G if for every dense Gδ subset
G of G (or equivalently, for every comeager subset of G, by Lemma
3.5 below),
there exists an aﬃne map f : G → G such that f (A) ⊂G.
Example 3.2. For G = Rn, Aut( Rn) = GL(n, R) and the locally compact Polish
group aﬃne transformation coincides with the usual aﬃne transfo rmation on Rn.
Remark 3.3. In this section, we will use the following facts.
(1) If ϕ is an aﬃne transformation in a locally Polish group, then ϕ−1 is also an
aﬃne transformation, since an injective Borel measurable functio n maps Borel
sets to Borel sets [ 19, Corollary 15.2]
(2) An automorphism on a locally compact Polish group is a homeomorph ism.
This is because every Haar measurable homomorphism between locally com-
pact Polish groups is continuous, which is a result of Weil [ 34, page 50]. For
a recent generalization of this result to Polish groups that are not n ecessarily
locally compact, see [ 28].

TOPOLOGICAL ERD ˝OS SIMILARITY CONJECTURE AND SMZ SETS 7
Now, Conjecture 1.2 can be naturally generalized to locally compact Polish groups.
Conjecture 3.4. There is no uncountable topologically universal set in any l ocally
compact Polish group.
The main goal of this section is to show that the above conjecture is independent
of ZFC. We start with the following analogue of Lemma 2.2.
Lemma 3.5. A subset X of a locally compact Polish group G is topologically universal
if and only if X is universal in the family of all comeager sets in G.
Proof. Since Polish spaces are Baire spaces by Baire Category Theorem, Le mma 2.1
states that every dense Gδ subset of G contains a comeager subset of G and every
comeager subset of G contains a dense Gδ subset of G. This is suﬃcient to prove the
statement by the same logic as in Lemma 2.2. □
Next, we need the generalizations of strong measure zero sets.
Deﬁnition 3.6. (1) A metric space X is said to be strong measure zero if for
every sequence ( ǫn)∞
n=1 of positive reals, there exists a sequence ( Xn)∞
n=1 of
subsets of X such that diam(Xn)<ǫ n and X = ⋃ ∞
n=1Xn.
(2) A subset X of a topological group G is called Rothberger bounded if for
each sequence (Un)n∈N of neighborhoods of 1G, there exists a sequence ( gn)n∈N
such that X ⊂ ⋃
n∈N (gn ·Un).
We ﬁrst restrict our attention to Polish groups since the notion of R othberger
boundedness coincides with the notion of strong measure zero set s of any compatible
metric. This is a consequence of a result by Fremlin [
12, Corollary 534G].
Theorem C (Fremlin). If a topological group G is a Polish group, then a subset X of
G is Rothberger bounded if and only if X is of strong measure zero in G with respect
to every left-invariant metric on G that induces the topology of G.
Hence, we make the following deﬁnition.
Deﬁnition 3.7. A subset of a Polish group is a strong measure zero set if it is
Rothberger bounded.
The cardinality of strong measure zero subsets of Polish groups an d strong measure
zero metric spaces are closely related to the cardinality of strong m easure zero sets
in the real line, as shown in the following theorem.
Theorem D. The followings are equivalent.
(1) Borel conjecture (every strong measure zero subset of R is countable).
(2) Every strong measure zero metric space is countable.
(3) Every strong measure zero subset of a Polish group is coun table.

8 YEONWOOK JUNG AND CHUN-KIT LAI
Proof. (1 ⇒ 2) This is a result by Carlson [
5, Theorem 3.2], which shows that if
X is an uncountable strong measure zero metric space, then there e xists a Lipschitz
embedding from X into R. Using an elementary analysis argument, we can see that
images of strong measure zero sets under uniformly continuous fu nctions are strong
measure zero sets. As Lipschitz embedding is uniformly continuous, the proof is
complete.
(2 ⇒ 3) Suppose every strong measure zero metric space is countable. Let X be
a strong measure zero subset of a Polish group G. By Deﬁnition 3.7, X is Roth-
berger bounded. By Theorem C, for any left-invariant metric d on G that induces
the topology of G, X is a strong measure zero metric space. By assupmtion, X is
countable.
(3 ⇒ 1) This is true since R is a Polish group. □
Recall that the Galvin-Mycielski-Solovay (Theorem A) provides a profound char-
acterization of strong measure zero sets in R in terms of sumsets. A natural question
is the following: in generalizing strong measure zero sets, to what ex tent of spaces
do we have an analogue of Galvin-Mycielski-Solovay theorem? It turn s out that the
answer is locally compact Polish groups, as described in the following th eorem by
Kysiak in [ 21] and independently by Fremlin in [ 12]. For another source of proof, see
[17, Theorem 3.5].
Theorem E (Kysiak-Fremlin). If G is a locally compact Polish group, a subset X of
G is a strong measure zero set if and only if X ·M ̸= G for each meager set M in G.
The Galvin-Mycielski-Solovay theorem (Theorem E) does not hold for general
Polish groups. For example, in [ 16, Theorem 3.10], it was shown that, assuming
cov(M) = c, the Baer-Specker group ZN is an example of a Polish group that that is
not locally compact and that does not satisfy the Galvin-Mycielski-So lovay theorem.
Based on these observations, Hruˇ s´ ak and Zindulka conjectured that if we assume CH,
then the Galvin-Mycielski-Solovay theorem holds in a Polish group G and only if G
is locally compact [ 17, Conjecture 3.6].
We now prove a sumset characterization of topologically universal s ets in locally
Polish groups, namely, a generalization of Lemma 2.3 from R to any locally compact
Polish group.
Lemma 3.8. Let G be a locally compact Polish group. A subset X in G is topologically
universal if and only if for every meager set M in G, there exists ϕ ∈ Aut(G) such
that X ·ϕ−1(M) ̸= G
Proof. The proof is analogous to that of Lemma
2.3. We ﬁrst demonstrate the only if
part. Suppose X is a topologically universal subset of G. Let M be a meager subset
of G. Then, since group inversion is a homeomorphism and homeomorphism maps
meager sets to meager sets, M −1 = {x−1 : x ∈ M} is a meager subset of G. By
Lemma 3.5, there exists ψ ∈ Aut(G) and h ∈ G such that h ·ψ(X) ⊂ (M −1)c, i.e.,

TOPOLOGICAL ERD ˝OS SIMILARITY CONJECTURE AND SMZ SETS 9
(h ·ψ(X)) ∩M −1 = ∅. This implies that for all x ∈X and y ∈M, h ·ψ(x) ̸= y−1,
i.e., x · (ψ−1(y)) ̸=ψ−1(h−1). Hence, ψ−1(h−1) ̸∈X ·ψ−1(M), i.e., X ·ψ−1(M) ̸= G.
By taking ϕ =ψ−1 ∈ Aut(G), we have X ·ϕ(M) ̸= G.
Next, we show the if part. Let X be a subset of G and suppose that for every meager
set N in G, there exists ψ ∈ Aut(G) such that X ·ψ−1(N) ̸= G. Let M be a meager
subset of G. Again, since group inversion is a homeomorphism and homeomorphism
maps meager sets to meager sets, M −1 is a meager subset of G. Thus, there exists
ψ ∈ Aut(G) such that X ·ψ−1(M −1) ̸= G. This implies that there exists g ∈ G such
that for all x ∈ X and y ∈ M, x ·ψ(y−1) ̸= g, i.e., ψ−1(g−1) ·ψ−1(x) ̸= y. Hence,
by letting ϕ = ψ−1 ∈ Aut(G) and h = ψ−1(g−1), we have ( h ·ϕ(X)) ∩M = ∅, i.e.,
h ·ϕ(X) ⊂M c. Therefore, X is universal in comeager subsets of G, and by Lemma
3.5, X is topologically universal. □
We can now classify all topologically universal sets in a locally compact P olish
group in analogy with Theorem 2.4.
Theorem 3.9. A subset in a locally compact Polish group G is topologically universal
if and only if it is a strong measure zero set.
Proof. We ﬁrst prove the if part. Suppose X is a strong measure zero set in G. Then,
by Theorem
E, for every meager subset of G, we have X ·M ̸= G. By choosing ϕ to
be the identity map id G on G in Lemma 3.8, X is topologically universal in G.
Next, we prove the only if part. Suppose X is topologically universal. We are going
to show that X is Rothberger bounded. Let ( Un)n∈N be a sequence of neighborhoods
of 1G. Since G is a Polish group, there exists a countable neighborhood basis B =
{Bn : n ∈ N} of 1G. Since G is separable, letting ( gn)∞
n=1 be an enumeration of a
dense subset of G, ⋃ ∞
n=1gn ·Un is a dense open subset of G. Deﬁne
G =
∞⋂
k=1
∞⋃
n=1
gn · (Bk ∩Un).
Since G is a dense Gδ set, there exists an aﬃne map f = h · ϕ on G for some
ϕ ∈ Aut(G) and h ∈ G such that
f (X) = h ·ϕ(X) ⊂G.
This implies that
X ⊂
∞⋂
k=1
∞⋃
n=1
[(
ϕ−1(h−1 ·gn)
)
·
(
ϕ−1(Bk)
⋂
ϕ−1(Un)
)]
.
Since a Haar measurable automorphism in a locally compact Polish group is a home-
omorphism, ϕ is a homeomorphism (Remark
3.3). Since homeomorphisms preserve
neighborhood bases, {ϕ−1(Bk) : k ∈ N} is a neighborhood basis of 1G. Thus, there

10 YEONWOOK JUNG AND CHUN-KIT LAI
exists k ∈ N such that ϕ−1(Bk) ⊂Un. Hence,
X ⊂
∞⋃
n=1
[(
ϕ−1(h−1 ·gn)
)
·
(
ϕ−1(Bk)
⋂
ϕ−1(Un)
)]
⊂
∞⋃
n=1
(
ϕ−1(h−1 ·gn)
)
·Un =
∞⋃
n=1
g′
n ·Un,
where g′
n =ϕ−1(h−1 · (gn)). Therefore, X is a strong measure zero set in G. □
The following corollary, which states that Conjecture
3.4 is independent of ZFC, is
now immediate.
Corollary 3.10. The existence of an uncountable strong measure zero set in a l ocally
compact Polish group is independent of ZFC.
Proof. This directly follows from Theorem
3.9 and the Borel conjecture for locally
compact Polish groups (Theorem D). □
4. Measure-Category Duality and Open Questions
4.1. Measure-Category duality. In the literature of descriptive set theory and
mathematical logic, several results in measure theory are transf erred to analogous
results in category (meaning Baire category), and vice versa, by t he notion of measure-
category duality.
Theorem K (Erd˝ os-Sierpi´ nski). Assuming the continuum hypothesis ( CH), there
exists a bijection f : R → R such that f ◦f is the identity map on R and X is a
Lebesgue measure zero subset of R if and only if f (X) is a meager subset of R.
The mapping in Theorem
K is referred to as the Erd˝ os-Sierp´ nski mapping. The
measure-category duality is a principle that suggests if a statemen t that is formulated
in terms of Lebesgue measure zero sets and/or meager sets holds true, then its dual
statement, which is obtained by replacing Lebesgue measure zero s ets with meager
sets in the statement and vice versa, also holds true. It is notewor thy that although
the dual statement is easy to obtain, the Erd˝ os-Sierpi´ nski ma pping cannot be used
as a direct proof, thus often requiring a diﬀerent proof. This is bec ause the Erd˝ os-
Sierpi´ nski mapping requiresCH and it does not preserve addition [ 22], which implies
that it cannot directly prove any dual statements involving addition . Despite this,
this phenomenon of measure-category duality has been used in var ious situations [ 25].
Until now, we have classiﬁed all topologically universal sets and reso lved the topo-
logical variant of the Erd˝ os similarity conjecture posed by Gallagher, Lai, and Weber
in R and in locally compact Polish groups. In this section, we use the princip le
of duality between measure and category to translate our results in the topological
(category) setting to the measure-theoretic setting.

TOPOLOGICAL ERD ˝OS SIMILARITY CONJECTURE AND SMZ SETS 11
4.2. Full measure universality. We begin by introducing the dual notion of topo-
logically universal sets.
Deﬁnition 4.1. A subset of R is full measure universal if it is universal in the
family of all Lebesgue measurable sets with full measure, where a se t E has full
measure if R \E has zero Lebesuge measure.
Erd˝ os-Sierp´ nski mapping suggests that measure zero sets and meager sets can be
regarded as dual objects under CH. Taking the complement, sets with full measures
and comeager sets are dual to each other. Hence, we derive the f ollowing conjecture
as the dual of Conjecture
1.2.
Conjecture 4.2. There is no uncountable full measure universal subset in R.
The dual notions of strong measure zero sets and the Borel conj ecture are as follows.
Deﬁnition 4.3. A subset X of R is called strongly meager ifX +M ̸= R for every
Lebesgue measure zero set M in R. The dual Borel conjecture is the statement
that all strongly meager subsets of R are countable.
Similar to the Borel conjecture, the dual Borel conjecture is also known to be
independent of ZFC. The consistency of the negation of the dual Borel conjecture
is due to Pawlikowski and Janusz [ 27], where they showed that every Sierpi´ nski set,
which is an uncountable subset of R that intersects every Lebesgue measure zero
set countably, is a strongly meager set. Since Sierpi´ nski sets ex ist assuming CH,
this proves the consistency of the negation of the dual Borel con jecture in ZFC. The
consistency of the dual Borel conjecture is due to Carlson. A det ailed review of the
dual Borel conjecture can be found in [ 2, Chapter 8], and recent generalizations and
developments can be found in [ 29].
Proposition 4.4. A subset X of R is full measure universal if and only if for every
Lebesuge measure zero set M in R, there exists λ ̸= 0 such that X +λM ̸= R.
Consequently, strongly meager sets are full measure univer sal.
Proof. The ﬁrst part of the proof is identical to the proof of Lemma 2.3 by substituting
Lebesgue measure zero sets in place of meager sets.
To see the second part, let X be a strongly meager set. Then by the deﬁnition of
strongly meager set, X satisﬁes the ﬁrst part of the statement with λ = 1. Thus, X
is a full measure universal set in R. □
Using strongly meager sets, it is natural to pose the following classiﬁ cation conjec-
ture for full measure universal sets, which is the dual of Theorem 2.4.
Conjecture 4.5. A subset of R is full measure universal if and only if it is a strongly
meager subset of R.
Remark 4.6. We make few remarks on Conjectures 4.2 and 4.5.

12 YEONWOOK JUNG AND CHUN-KIT LAI
(1) Note that Conjecture 4.2 can also be viewed as the uncountable version of
the original Erd˝ os similarity conjecture (Conjecture 1.1). To the best of our
knowledge, Conjecture 4.2 and Conjecture 1.1 do not imply each other.
(2) The validity of Conjecture 4.5 will imply that Conjecture 4.2 is independent
of ZFC by the fact that dual Borel conjecture is independent of ZFC, which,
together with Theorem 2.4, conﬁrms the principle of duality between measure
and category.
(3) As mentioned in Remark 2.6, strong measure zero sets form a σ-ideal. This
motivated Prikry to conjecture that strongly meager sets also fo rm a σ-ideal.
However, it turns out that if one assumes CH, then strongly meager sets actu-
ally do not form a σ-ideal, as shown by Bartoszy´ nski and Shelah in [ 3]1. We
ask the following question:
(Qu): Do full measure universal sets form σ-ideals?
If the answer is yes, then assuming CH, the set of all strongly meager sets
is a strict subset of the set of all strong measure zero sets. This p roduces a
model of ZFC in which Conjecture 4.5 is false, proving that the negation of
the Conjecture 4.5 is consistent in ZFC. We note that we do not yet know if
Conjecture 4.5 is consistent in ZFC, in which case, Conjecture 4.5 would be
independent of ZFC.
(4) The measure-category duality (Theorem K) extends to arbitrary locally com-
pact Polish groups. This allows one to deﬁne full measure universal s ets and
strongly meager sets in locally Polish group as the dual of strong mea sure
zero sets via the Galvin-Mycielski-Solovay theorem (Theorem E): a set X in
a locally compact Polish group G is full measure universal if it is universal in
full Haar measure sets in G, and X is strongly meager if X +M ̸= G for all
Haar measure zero subsets M of G.
4.3. Perfect sets. Unfortunately, Conjecture 4.5 is open even for perfect sets. Erd˝ os,
Kunen, and Mauldin [ 9] showed that perfect sets are not strongly meager.
Theorem 4.7 (Erd˝ os-Kunen-Mauldin). For every perfect set P ⊂ R, there exists a
set M ⊂ R of zero Lebesgue measure such that P +M = R.
Erd˝ os-Kunen-Mauldin theorem does not imply that perfect sets are not full measure
universal because we do not know if the same M works for all λ ̸= 1 in Lemma 4.4.
Hence, we pose the following generalization of the Erd˝ os-Kunen-Mauldin Theorem as
a conjecture, which would imply that all perfect sets are not full me asure universal
using Proposition 4.4.
Conjecture 4.8. Let P ⊂ R be a perfect set. Then, there exists a set M ⊂ R with
Lebesgue measure zero such that P +λM = R for all λ ̸= 0.
1This is an example of a subtlety in following the principle of measure-cat egory duality. It often
suggests dual results that turn out to be correct, but not alway s. As shown in this case, strongly
meager sets sometimes behave worse than strong measure zero s ets.

TOPOLOGICAL ERD ˝OS SIMILARITY CONJECTURE AND SMZ SETS 13
Conjecture 4.5 and Conjecture 4.8 will resolve a stronger version of the Erd˝ os
similarity conjecture for perfect sets. Finally, we conclude this sec tion with a suﬃcient
condition for Conjecture 4.8, which only require robustness under arbitrarily small
amount of scaling.
Proposition 4.9. Suppose that for all compact perfect set P , there exist ǫ0 > 0,δ >0
and a compact set K with zero Lebesgue measure such that P +tK contains an open
interval of length ǫ0 for all t ∈ (1 −δ, 1]. Then, there exists an Fσ set M satisfying
Conjecture
4.8.
Proof. Let 1 < a< 1
1−δ . Then, all consecutive intervals ( aj(1 −δ),a j] and (aj+1(1 −
δ),a j+1] overlap. Moreover, as a> 1,
⋃
j∈Z
(aj(1 −δ),a j] = (0, +∞). (1)
Deﬁne
M =
⋃
j∈Z
⋃
k∈Z
aj (K +ǫ0k).
ThenM clearly has zero Lebesgue measure. Note that by (1), for each λ> 0, we can
ﬁnd j ∈ Z so that t := a−jλ ∈ (1 −δ, 1]. Let I be the open interval inside P +tK
with length ǫ0. Then, since λa−j ≤ 1, we have
P +λM ⊃P +λ
⋃
k∈Z
a−j (K +ǫ0k) ⊃
⋃
k∈Z
(I +ǫ0tk) = R.
□
Such compact setK can easily be constructed if P has positive Newhouse thickness,
in which case, one can use the Newhouse gap lemma. This recovers th e result that
Cantor sets with positive Newhouse thickness are not full-measure universal in [ 13,
Theorem 1.5]. We were also informed by P. Shmerkin that the same is als o true if P
has positive Hausdorﬀ dimension using a probabilistic argument in [ 30, Theorem 13.1]
(an argument is outlined in [ 18]). We do not have a deﬁnitive answer to Conjecture
4.8 if Cantor set has both Hausdorﬀ dimension and Newhouse thickness zero.
Acknowledgments The authors thank Daeseok Lee, Krystal Taylor, Alex McDon-
ald, and Matthew Foreman for helpful discussions.
References
1. Tomek Bartoszy´ nski and Haim Judah, Set theory , A K Peters, Ltd., Wellesley, MA, 1995, On
the structure of the real line. MR 1350295
2. , Set theory: On the structure of the real line , 1995.
3. Tomek Bartoszy´ nski and Saharon Shelah,Strongly meager sets do not form an ideal , J. Math.
Log. 1 (2001), no. 1, 1–34. MR 1838340
4. Jean Bourgain, Construction of sets of positive measure not containing an a ﬃne image of a
given inﬁnite structures , Israel J. Math. 60 (1987), no. 3, 333–344. MR 937795
5. Timothy J. Carlson, Strong measure zero and strongly meager sets , Proceedings of the American
Mathematical Society 118 (1993), no. 2, 577–586.

14 YEONWOOK JUNG AND CHUN-KIT LAI
6. Stanley J. Eigen, Putting convergent sequences into measurable sets , Studia Sci. Math. Hungar.
20 (1985), no. 1-4, 411–412. MR 886044
7. ´Emile Borel, Sur la classiﬁcation des ensembles de mesure nulle , Bulletin de la Soci´ et´ e
Math´ ematique de France47 (1919), 97–125 (fr).
8. Paul Erd˝ os,Problems, Math. Balkanica (Papers presented at The Fifth Balkan Mathemat ical
Congress), 4(1974), 203–204. MR 55:2715
9. Paul Erd˝ os, Kenneth Kunen, and Richard D. Mauldin, Some additive properties of sets of real
numbers, Fundamenta Mathematicae 113 (1981), 187–199.
10. Kenneth Falconer, On a problem of Erd˝ os on sequences and measurable sets, Proc. Amer. Math.
Soc. 90 (1984), no. 1, 77–78. MR 722418
11. Matthew Foreman and Akihiro Kanamori (eds.), Handbook of set theory. Vols. 1, 2, 3 , Springer,
Dordrecht, 2010. MR 2768678
12. David H. Fremlin, Measure theory. vol. 5, set-theoretic measure theory , Torres Fremlin, Colch-
ester, 2015.
13. John Gallagher, Chun-Kit Lai, and Eric Weber, On a topological Erd˝ os similarity problem, Bull.
Lond. Math. Soc. 55 (2023), no. 3, 1104–1119. MR 4599101
14. Fred Galvin, Jan Mycielski, and Robert M. Solovay, Strong measure zero sets , Notices of the
American Mathematical Society 26, A–280. (1973).
15. , Strong measure zero and inﬁnite games , Archive for Mathematical Logic 56 (2017),
no. 7-8, 725–732.
16. Michael Hruˇ s´ ak, Wolfgang Wohofsky, and Ondˇ rej Zindulka,Strong measure zero in separable
metric spaces and polish groups , Arch. Math. Logic 55, 105–131 (2016).
17. Michael Hruˇ s´ ak and Ondˇ rej Zindulka,Strong measure zero in polish groups , 2019.
18. Yeonwook Jung, Chun-Kit Lai, and Yuveshen Mooroogen, Fifty years of the erd˝ os similarity
conjecture, Res. Math. Sci. 12 (2025), no. 1, Paper No. 9. MR 4852289
19. Alexander S. Kechris, Classical descriptive set theory , Graduate Texts in Mathematics, vol. 156,
Springer-Verlag, New York, 1995. MR 1321597
20. Mihalis Kolountzakis, Inﬁnite patterns that can be avoided by measure , Bull. London Math. Soc.
29 (1997), no. 4, 415–424. MR 1446560
21. Marcin Kysiak, On erd˝ os-sierpi´ nski duality between lebesgue measure and baire category (in
polish), Master’s thesis (2000).
22. Marcin Kysiak, Another note on duality between measure and category , Bull. Polish Acad. Sci.
Math. 51 (2003), no. 3, 269–281. MR 2017003
23. Richard Laver, On the consistency of borel’s conjecture, Acta Mathematica 137 (1976), no. none,
151 – 169.
24. Nikolai Luzin, Sur la classiﬁcation de m. baire , 1917, pp. 91—-94.
25. J. C. Oxtoby, Measure and category, A Survey of the Analogies between Topological and Measure
Spaces, Springer New York, NY, 2 ed., 2019.
26. John C. Oxtoby, Measure and category , second ed., Graduate Texts in Mathematics, vol. 2,
Springer-Verlag, New York-Berlin, 1980, A survey of the analogies between topological and
measure spaces. MR 584443
27. Janusz Pawlikowski, Every Sierpi´ nski set is strongly meager, Archive for Mathematical Logic 35
(1996), no. 5, 281–285.
28. Christian Rosendal, Continuity of universally measurable homomorphisms , Forum of Mathemat-
ics, Pi 7 (2019), e5.
29. Marion Scheepers and Ondrej Zindulka, Centenary of the borel conjecture , Contemporary Math-
ematics (2020).
30. Pablo Shmerkin and Ville Suomala, Spatially independent martingales, intersections, and ap pli-
cations, Mem. Amer. Math. Soc. 251 (2018), no. 1195, v+102. MR 3756896

TOPOLOGICAL ERD ˝OS SIMILARITY CONJECTURE AND SMZ SETS 15
31. Wac/suppress law Sierpi´ nski,Sur un ensemble non d´ enombrable, dont toute image continue est de mesure
nulle, Fundamenta Mathematicae 11(1) (1928), 302–304 (fr).
32. Hugo Steinhaus, Sur les distances des points dans les ensembles de measure po sitive, Fund.
Math. (1920), no. 1, 93–104.
33. R. E. Svetic, The Erd˝ os Similarity Problem, Real Analysis Exchange 26 (2000), no. 2, 525 –
540.
34. Andr´ e Weil,L’integration dans les groupes topologiques et ses applica tions, 1951.
University of California, Irvine, Department of Mathemati cs, Rowland Hall,
Irvine, CA 92697
Email address : yeonwoj1@uci.edu
San Francisco State University Department of Mathematics, 1600 Holloway A ve,
San Francisco, CA 94132
Email address : cklai@sfsu.edu