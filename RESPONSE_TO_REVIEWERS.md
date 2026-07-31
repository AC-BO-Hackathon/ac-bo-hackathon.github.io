# Response to Reviewers

**Manuscript:** DD-ART-06-2026-000353 — *Bayesian Optimization Hackathon for Chemistry and Materials*

We thank the four referees for their careful and constructive reports, and for their generous
assessment of the hackathon as a community-resource contribution. The common thread across the
reports is that the manuscript should do more than list projects: it should synthesize what the
event taught us, organizationally and scientifically, and point forward. We have restructured the
back half of the paper accordingly, adding three new sections:

- **Cross-Project Synthesis** — a classification of all 45 outputs by primary deliverable, a
  repository-license tabulation, and a discussion of commonalities, differences, and participant
  expertise.
- **Lessons Learned** — an organizational retrospective (what worked, what did not, what we would
  change) and a discussion of the strengths and limitations of Bayesian optimization (BO) revealed
  by the projects.
- **Future Opportunities** — a forward-looking section covering the directions the referees named.

We have also completed the project listing (the six previously omitted projects are now included),
corrected the flagged tables, figures, and links, and made the summarization workflow and its
limitations explicit. Throughout the new material we state plainly that the synchronous event
spanned only two days, so the projects are best read as rapid feasibility studies rather than
validated results; we have tried to avoid over-claiming on that basis.

A latexdiff PDF marking all changes relative to the originally submitted version accompanies this
response.

Referee comments are quoted below in blockquotes, with our replies interspersed.

---

## Referee 1

> The manuscript reports the organization and outputs of the AC-BO Hackathon 2024, a two-day virtual
> event focused on Bayesian optimization for chemistry and materials. I view the event itself as a
> valuable community effort. [...] This is a meaningful contribution to the community, especially
> because practical examples and reusable code for Bayesian optimization in chemistry and materials
> remain scattered across different packages and application domains.
>
> A particular strength of the manuscript is the open-resource aspect. [...]

Thank you — we appreciate this assessment, and we have tried to make the revision strengthen exactly
the resource aspect you highlight.

> However, I think the manuscript would be significantly strengthened by adding more synthesis rather
> than only listing individual project summaries. First, the authors should summarize the
> organizational lessons learned from running the hackathon. For example, what worked well in terms
> of pre-event tutorials, GitHub classroom assignments, virtual collaboration tools, team formation,
> project scoping, judging, mentoring, and post-event archiving? What did not work well? What would
> the organizers change in a future event?

Added as **Lessons Learned → Organizational lessons**. Briefly: the pre-event preparation (orientation
materials, intro-to-BO content, curated tooling, and a Python refresher delivered via GitHub
Classroom with automated feedback), the persistent Gather Town venue, the Gavel pairwise judging
system, and the GitHub-plus-Zenodo archiving all worked and would be retained. What did not work as
well: some registered teams never converged into active projects, six teams recorded no closing
video, the two-day window limited validation depth, and participant code reproducibility varied
widely. The same subsection lists four concrete changes we would make (earlier structured team
formation, explicit reproducibility/licensing checklists, a required short summary from every team,
and clearer communication of evaluation expectations).

> Second, the authors should synthesize the scientific lessons from the project outcomes. [...] I
> encourage the authors to add a section summarizing the observed pros and cons of BO across the
> projects. For example, the paper could discuss where BO performed well [...]. It should also
> discuss limitations identified by the projects, such as sensitivity to molecular representation,
> kernel choice, warm-start data, noisy observations, high-dimensional search spaces, batch-size
> selection, acquisition-function optimization, computational overhead, and reproducibility of
> benchmark comparisons.

Added as **Lessons Learned → Scientific lessons: strengths and limitations of Bayesian optimization**.
On the strengths side we discuss sample efficiency in low-data regimes and the breadth of problem
types the teams handled (continuous, categorical, mixed, molecular, multi-objective, multi-fidelity,
contextual, batched, cost-aware, and preference-based). On the limitations side we give concrete
project-anchored examples: BO was comparable to random search in project 33 and an off-the-shelf
method underperformed random candidates on the narrow benchmark of project 1; project 3 showed that
acquisition-optimizer runtime materially changed observed performance. We also discuss sensitivity
to representation and kernel choice, warm-start quality, noise, and high dimensionality, and note
that retrospective benchmark gains do not guarantee wet-laboratory success. New citations support
each point.

> Third, the authors should add a forward-looking section on future opportunities for Bayesian
> optimization in materials discovery. [...] Possible topics include BO for autonomous laboratories,
> multi-fidelity optimization, uncertainty-aware experimental planning, foundation-model-assisted BO,
> preference-based BO, multi-objective materials design, robust BO under noisy experimental data,
> benchmark development, and domain-specific BO tools for synthesis and processing optimization.

Added as **Future Opportunities**, which covers each of the directions you list, with references. We
also flag there that roughly one in six hackathon projects incorporated large language models, which
we treat as a signal for the foundation-model-assisted BO direction while noting recent evidence
that LLM-based surrogates and priors do not yet consistently beat strong classical baselines.

> I also recommend that the authors provide a more systematic evaluation of the 45 project outputs.
> It would be helpful to classify projects into categories such as mature software, benchmark
> datasets, tutorials, application demonstrations, and preliminary concepts. A table reporting code
> availability, licensing, documentation, reproducibility, dependency status, and maintenance plans
> would strengthen the resource value of the paper.

Added as **Cross-Project Synthesis → Classification of project outputs**, using exactly the five
categories you propose (Table 3: application demonstration 24, preliminary concept 8, benchmark
dataset/problem 6, tutorial/educational 4, mature software 3). Code availability and licensing are
reported in the accompanying text and in Table 4 (license distribution across the 40 distinct linked
repositories, queried programmatically via the GitHub API): 25 of the 36 accessible repositories
carry an explicit license, overwhelmingly permissive, while 11 have none. On documentation,
dependency status, and maintenance plans we report the aggregate finding rather than a per-project
column: dependency specifications were frequently incomplete and few teams stated a maintenance
plan, so we describe the outputs as reusable starting points that generally require further
engineering. The license tabulation is produced by a script archived with the manuscript source so
that it can be re-run and updated.

> Overall, I find the manuscript valuable as a community-resource and open-science contribution. [...]
> I recommend major revision to add a stronger synthesis of organizational lessons, scientific
> lessons from the BO applications, limitations revealed by the project outcomes, and future
> opportunities for Bayesian optimization in chemistry and materials.

We hope the three new sections meet this. Thank you for a report that materially improved the paper.

---

## Referee 2

> This paper summarizes the findings arising from the organization of a hackaton on BO methods
> applied to chemistry and materials science. I believe that there is a lot of value in presenting
> the details on how the hackaton was organized [...]. Other novel aspects such as the method used
> for evaluating the teams to select the best ones are also state-of-the-art and are worthy of
> dissemination.

Thank you.

> My only recommendation is for the authors to present a meta-analysis of the different projects,
> beyond summary listings of the project titles and the description of the individual projects. For
> example, were there commonalities/differences in the way different teams approach their problems?

Addressed in **Cross-Project Synthesis → Commonalities, differences, and participant expertise**. A
common template recurs across the projects: frame the task as sequential optimization of an expensive
objective with a Gaussian-process surrogate and an acquisition function, usually on
BoTorch/GPyTorch or Ax, sometimes through domain wrappers such as BayBE or GAUCHE. Teams differed
most in three respects — the representation of inputs, whether they compared against a simple
baseline such as random search, and whether they targeted real experimental data or retrospective
benchmarks.

> Does the level of prior expertise impact the outcomes?

Discussed in the same subsection. We report that participants ranged from students to senior
researchers across academia, industry, and government, and that mixed-expertise teams pairing domain
scientists with BO practitioners appeared to be an asset. We are explicit that we did not run a
controlled study, and that apparent performance differences may reflect problem difficulty or the
availability of warm-start data rather than expertise or method choice.

> Are there follow up studies to see whether participants are applying BO methods in their own
> research? What was the ultimate gain from the hackaton? increased awareness? increased
> understanding of the methods? more interactions across many groups?

We did not run a longitudinal follow-up survey, and we say so rather than infer outcomes we did not
measure; the broader hackathon literature notes that such follow-up data are generally scarce. What
we can report, and do, is qualitative persistence: contributions folded into the maintained GAUCHE
library, a community-curated resource list (project 43), the archived and citable Zenodo record, and
a durable community around the event — mirroring the persistent communities reported for the sibling
LLM-for-chemistry hackathons. Regarding the gains: the event's stated aims were new connections, new
skills, and new ideas, and the outputs and the demographic breadth in Fig. 2 speak to awareness and
cross-group interaction more directly than to measured skill gain.

> While I would not expect the authors to address all the items presented above, it would be very
> useful to have a reflective component to the paper and at least some discussion on lessons learned.

The **Lessons Learned** section is intended as exactly that reflective component; please see the
reply to Referee 1's first point for its structure.

---

## Referee 3

> Bayesian Optimization Hackathon for Chemistry and Materials documents a community output of the
> AC-BO Hackathon in 2024. [...] This article is interestingly documented. In fact, I really enjoyed
> it as a reader, because it gives many use cases (with code!) where BO may be useful.

Thank you.

> Although the article discusses each project individually and gives a good notion of what each
> project attempted to do / did, this reviewer finds the listing of projects to end a bit abruptly.
> It would be nice if some takeaways from the hackathon are produced at the end:

Agreed — the manuscript no longer ends with the project listing. Three synthesis sections now follow
it (Cross-Project Synthesis, Lessons Learned, Future Opportunities).

> 1. are there agreed upon frameworks that work better for specific tasks (i.e. with noisy data or
> less noisy data)?

Addressed at the end of **Lessons Learned → Scientific lessons**. Our reading is that there is no
universal winner: for low-noise, near-deterministic objectives, standard GP-based BO with expected
improvement remains a reasonable default, whereas noisy, heteroscedastic, or multi-objective settings
benefit from noise-robust acquisitions and from tooling built for the experimental setting
(e.g., BayBE, BoFire). We present this as a directional observation from short feasibility studies,
not as a benchmark verdict.

> 2. Are BO tools going to be easily deployable in experimental data settings (the hackathon seems to
> imply that it will!).

Addressed in the same subsection and in **Future Opportunities**. The honest answer from these
outputs is "not yet, uniformly": the projects show that deployment-oriented libraries have closed
much of the gap, but they also show that results are sensitive to representation, kernel, warm-start
quality, and noise, and that retrospective benchmark gains do not transfer automatically to the
laboratory. We name domain-specific, deployment-ready tooling for synthesis and processing
optimization as a priority direction.

> 3. Where is it useful to use Bayesian Optimization vs. where did end users find little utility?

Addressed with project-anchored examples in **Lessons Learned → Scientific lessons**: BO was most
useful in low-data, expensive-evaluation, multi-objective, and structured-input settings; it offered
little advantage over random search in project 33, and underperformed random candidates on the narrow
benchmark of project 1. We use these as arguments for always including a simple baseline rather than
as general verdicts on the methods.

> However, this reviewer also commends the fantastic effort in making everyone's data and code
> publicly available.

Thank you.

---

## Referee 4 (Data review)

> The authors summarize the results of a Hackathon focusing on Bayesian optimization algorithms,
> benchmark development, tutorialization, and problem definition [...]. While many of the projects
> which came from this event may not, in terms of their data and code, adhere to the standards of
> Digital Discovery, this summary report generally does.

Thank you. The specific items are addressed below.

### Major comments

> 1. The main text skips project 14, 19, 23, 29, 34, and 42. Can the authors indicate why these
> projects were withheld and update the introductory statement "This section provides a comprehensive
> summary and highlights the key findings from all project submissions" to reflect these omissions?

These projects were not withheld; their omission was an artifact of the summarization pipeline. The
summaries were generated from the closing-video submissions, and these six teams did not submit a
recorded video, so the pipeline produced no entry for them and this was not caught before submission.
All six now appear in **Projects' Key Findings**, written manually from the teams' project pages and
code repositories, with that provenance stated at the end of each summary. The introductory paragraph
has been rewritten to describe the pipeline and to state explicitly how the six no-video projects
were handled. All 45 projects are now present in both the main text and Table 1.

> 1a. For example, a reader would likely want to know more about the first- and second-place winners
> (projects 23 and 34).

Agreed. Projects 23 ("Reliable Surrogate Models of Noisy Data", first place) and 34 ("Streamlining
Material Discovery — Bayesian Optimization in Thermal Fluid Mixtures", second place) now have full
summaries in **Projects' Key Findings**, each noting its award.

> 2. Many of the code repositories do not provide adequate module requirement. (Projects 2–8, 10–16,
> 18, 20, 22–24, 26, 28, 33, & 38–41.) As this work is spotlighting contributions rather than
> presenting code as part of its research workflow, the Journal requirements for code repository
> metadata may not apply.

We agree with your reading and, rather than retro-fitting participants' repositories, we now report
the issue in the paper: **Cross-Project Synthesis → Classification of project outputs** states that
dependency specifications were frequently incomplete and that few teams articulated a maintenance
plan, and describes the outputs as reusable starting points that typically require further
engineering. **Lessons Learned → Organizational lessons** commits to providing explicit
reproducibility and licensing checklists (pinned dependencies, a runnable notebook, an appropriate
license) at future events.

> 3. There are some projects for which the dataset used is not clear. (Projects 6, 19–21, 29, 30, 31,
> 36, 37, 40, 42, & 45; project 15 provides the dataset, but it is buried within the code
> repository.)

This is outside our control for participant-authored repositories, but it is now disclosed rather
than left implicit, in the same passage cited above. The classification table and the surrounding
text are intended to let a reader see at a glance which outputs are immediately reusable and which
are not.

> 4. Can the rubric used for evaluating projects be included in the supplemental materials?

There was no numeric scoring rubric to include: judging used Gavel's holistic pairwise comparison,
in which judges rank projects against one another rather than scoring them on criteria. We have made
this explicit in **Lessons Learned → Organizational lessons**, which also points to the material that
did function as evaluation criteria — the instructions given to judges together with the submission
and authorship requirements — documented on the hackathon website and archived in the Zenodo record.

> 5. The workflow for transcribing and analyzing the projects is not reproducible at its current
> level of detail. Furthermore, the claim that this approach provides a structured and objective
> assessment of the submissions is not supported by any evidence or reference to prior works.

The opening of **Projects' Key Findings** has been rewritten. It now states the model and temperature
used, that the same prompt and settings were applied uniformly across submissions, that every draft
was manually reviewed and edited by the organizers, that the resulting per-project summaries are
archived with the manuscript source, and how the six no-video projects were handled instead. We have
withdrawn the "structured and objective assessment" claim: the text now says the summaries are
concise, uniformly generated descriptions of what each team set out to do and reported, and
explicitly not an independent or objective evaluation of technical merit.

### Tables and figures

> 6. Figure 2: The black text which falls above the map can be difficult to read.

Fixed. The inset histograms are drawn over the map, so their category labels and panel titles sat
directly on the map imagery. A light backing plate has been inserted behind the tick-label band and
behind each panel title, restoring contrast; the caption notes this. The transformation is applied by
a script archived with the manuscript source.

> 7. Table 1 spans two pages but contains no entries on the second page.

Fixed. Two problems were at work. First, rows were emitted in spreadsheet insertion order rather than
project order, so late-added projects rendered after project 45; the generating script now sorts by
project number. Second, the table's own layout allowed the closing rule to spill onto a page of its
own; the row spacing and column widths have been adjusted so that the table breaks cleanly and every
page carries entries.

> 9. Figure 3: The caption contains a statement on preprint server policies which should be updated to
> adhere to Digital Discovery's polices.

Fixed. The sentence "Image is blurred per preprint server policy" has been replaced with a statement
of the actual reason for the redaction: portions of the screenshot are blurred to protect potentially
identifying information.

> 11. Table 2: The "Prize" header is marked for a footnote that is not present.

Fixed. The footnote has been added: the first value is the prize awarded to each team member, and the
value in parentheses is the maximum total prize per team.

> 13. Figures 4 & 5: Were participants informed that their names and commentary may be made public
> prior to joining the event?

They were not, so we have redacted them. Participant display names are now pixelated throughout the
keynote-room panel of Fig. 4 and throughout the poster room of Fig. 5; the project and room labels are
retained, as are the names of the co-authors of this manuscript, who have consented. Both captions
state this. The redaction is applied by the same archived script.

### Minor comments

> 11. The use of project title headings as links to videos (hosted on YouTube) does not adhere to
> transparent hyperlink standards and is inaccessible on paper copies. In addition, these hyperlinks
> are redundant with the links already provided in Table 1.

Fixed. Project-title headings in **Projects' Key Findings** are now plain text; the video, repository,
and social-media links remain in Table 1, where they are visible as links.

> 13a. Project 40 has been migrated from the github listed on its project page to the repo listed in
> the Zenodo metadata file.
> 13b. Projects 33 and 34 do not have github links on their project pages despite having links in the
> Zenodo metadata file.

Fixed on the project pages and in Table 1: project 40 now points to the migrated repository, and
projects 33 and 34 now carry their repository links. A stale link on the project 42 page (which
pointed at a fork of the hackathon website rather than a project repository) has been removed.

> 13. Typographical errors in the Acknowledgement section, around the header for Project 3, and in the
> Author Contributions section. ("Ryan-Rhys Gri ths", "Jakub LÆla", "Can zkan", "Adrian o†i¢",
> "Je rey Watchorn", and potentially others.) Multiple ligatures appear to have been deleted ("fi",
> "ff", etc.).

Fixed. The names are correct in the LaTeX source; the corruption was in the compiled PDF, where the
f-ligature and accented glyphs lacked correct ToUnicode mappings and so were dropped on text
extraction. We now emit glyph-to-Unicode mappings (`\input glyphtounicode` with `\pdfgentounicode=1`),
which makes these names extract and copy correctly. We have checked the affected names — Ryan-Rhys
Griffiths, Jakub Lála, Can Özkan, Adrian Šošić, Jeffrey Watchorn — in the recompiled PDF.

### Data reviewer checklist

We note the checklist items marked "outside the control of the authors" and have not attempted to
modify participants' repositories. The two items pointing back to comment 5 (potential biases in the
source dataset; description of the summarization pipeline) are addressed by the rewritten opening of
**Projects' Key Findings** and by the scripts archived with the manuscript source, which include the
table-generation, summary-generation, repository-license, and figure-preparation code.
