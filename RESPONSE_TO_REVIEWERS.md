# Response to Reviewers

**Manuscript:** DD-ART-06-2026-000353, *Bayesian Optimization Hackathon for Chemistry and Materials*

Referee comments are quoted below, with replies interspersed.

---

## Referee 1

> The manuscript reports the organization and outputs of the AC-BO Hackathon 2024, a two-day virtual
> event focused on Bayesian optimization for chemistry and materials. I view the event itself as a
> valuable community effort. [...] This is a meaningful contribution to the community, especially
> because practical examples and reusable code for Bayesian optimization in chemistry and materials
> remain scattered across different packages and application domains.
>
> A particular strength of the manuscript is the open-resource aspect. [...]

Noted.

> However, I think the manuscript would be significantly strengthened by adding more synthesis rather
> than only listing individual project summaries. First, the authors should summarize the
> organizational lessons learned from running the hackathon. For example, what worked well in terms
> of pre-event tutorials, GitHub classroom assignments, virtual collaboration tools, team formation,
> project scoping, judging, mentoring, and post-event archiving? What did not work well? What would
> the organizers change in a future event?

Added as Lessons Learned, Organizational lessons.

> Second, the authors should synthesize the scientific lessons from the project outcomes. [...] I
> encourage the authors to add a section summarizing the observed pros and cons of BO across the
> projects. For example, the paper could discuss where BO performed well [...]. It should also
> discuss limitations identified by the projects, such as sensitivity to molecular representation,
> kernel choice, warm-start data, noisy observations, high-dimensional search spaces, batch-size
> selection, acquisition-function optimization, computational overhead, and reproducibility of
> benchmark comparisons.

Added as Lessons Learned, Scientific lessons: strengths and limitations of Bayesian optimization.

> Third, the authors should add a forward-looking section on future opportunities for Bayesian
> optimization in materials discovery. [...] Possible topics include BO for autonomous laboratories,
> multi-fidelity optimization, uncertainty-aware experimental planning, foundation-model-assisted BO,
> preference-based BO, multi-objective materials design, robust BO under noisy experimental data,
> benchmark development, and domain-specific BO tools for synthesis and processing optimization.

Added as Future Opportunities, which covers each direction listed.

> I also recommend that the authors provide a more systematic evaluation of the 45 project outputs.
> It would be helpful to classify projects into categories such as mature software, benchmark
> datasets, tutorials, application demonstrations, and preliminary concepts. A table reporting code
> availability, licensing, documentation, reproducibility, dependency status, and maintenance plans
> would strengthen the resource value of the paper.

Added as Cross-Project Synthesis: classification in Table IV, per-project license status in Table V,
per-project assignments in the ESI.

> Overall, I find the manuscript valuable as a community-resource and open-science contribution. [...]
> I recommend major revision to add a stronger synthesis of organizational lessons, scientific
> lessons from the BO applications, limitations revealed by the project outcomes, and future
> opportunities for Bayesian optimization in chemistry and materials.

Addressed by the three new sections above.

---

## Referee 2

> This paper summarizes the findings arising from the organization of a hackaton on BO methods
> applied to chemistry and materials science. I believe that there is a lot of value in presenting
> the details on how the hackaton was organized [...]. Other novel aspects such as the method used
> for evaluating the teams to select the best ones are also state-of-the-art and are worthy of
> dissemination.

Noted.

> My only recommendation is for the authors to present a meta-analysis of the different projects,
> beyond summary listings of the project titles and the description of the individual projects. For
> example, were there commonalities/differences in the way different teams approach their problems?

Added as Cross-Project Synthesis; see the manuscript.

> Does the level of prior expertise impact the outcomes?

Cross-Project Synthesis notes the mix of participant backgrounds; outcomes were not measured by
expertise.

> Are there follow up studies to see whether participants are applying BO methods in their own
> research? What was the ultimate gain from the hackaton? increased awareness? increased
> understanding of the methods? more interactions across many groups?

No follow-up survey was run. Persistence of outputs and a commitment to survey participants at
future events are stated in Lessons Learned, Organizational lessons.

> While I would not expect the authors to address all the items presented above, it would be very
> useful to have a reflective component to the paper and at least some discussion on lessons learned.

Added as Lessons Learned.

---

## Referee 3

> Bayesian Optimization Hackathon for Chemistry and Materials documents a community output of the
> AC-BO Hackathon in 2024. [...] This article is interestingly documented. In fact, I really enjoyed
> it as a reader, because it gives many use cases (with code!) where BO may be useful.

Noted.

> Although the article discusses each project individually and gives a good notion of what each
> project attempted to do / did, this reviewer finds the listing of projects to end a bit abruptly.
> It would be nice if some takeaways from the hackathon are produced at the end:

The manuscript no longer ends with the project listing: Cross-Project Synthesis, Lessons Learned,
and Future Opportunities follow it.

> 1. are there agreed upon frameworks that work better for specific tasks (i.e. with noisy data or
> less noisy data)?

The projects support only a narrow observation here; see the end of Lessons Learned, Scientific
lessons.

> 2. Are BO tools going to be easily deployable in experimental data settings (the hackathon seems to
> imply that it will!).

Addressed in Lessons Learned, Scientific lessons and in Future Opportunities, which now also cites
graphical and web-based BO interfaces.

> 3. Where is it useful to use Bayesian Optimization vs. where did end users find little utility?

Project-anchored examples are in Lessons Learned, Scientific lessons; without a participant survey
we do not generalize beyond them.

> However, this reviewer also commends the fantastic effort in making everyone's data and code
> publicly available.

Noted.

---

## Referee 4 (Data review)

> The authors summarize the results of a Hackathon focusing on Bayesian optimization algorithms,
> benchmark development, tutorialization, and problem definition [...]. While many of the projects
> which came from this event may not, in terms of their data and code, adhere to the standards of
> Digital Discovery, this summary report generally does.

The items are addressed below.

### Major comments

> 1. The main text skips project 14, 19, 23, 29, 34, and 42. Can the authors indicate why these
> projects were withheld and update the introductory statement "This section provides a comprehensive
> summary and highlights the key findings from all project submissions" to reflect these omissions?

Not withheld: these six teams did not submit the closing video the summarization pipeline ran on.
Their summaries were written from the teams' project pages and public project outputs and added back
for completeness; see the opening of Projects' Key Findings. All 45 projects now appear in the text
and in Table III.

> 1a. For example, a reader would likely want to know more about the first- and second-place winners
> (projects 23 and 34).

Projects 23 and 34 now have full summaries in Projects' Key Findings, each noting its award.

> 2. Many of the code repositories do not provide adequate module requirement. (Projects 2–8, 10–16,
> 18, 20, 22–24, 26, 28, 33, & 38–41.) As this work is spotlighting contributions rather than
> presenting code as part of its research workflow, the Journal requirements for code repository
> metadata may not apply.

Noted. The aggregate finding is reported in Cross-Project Synthesis.

> 3. There are some projects for which the dataset used is not clear. (Projects 6, 19–21, 29, 30, 31,
> 36, 37, 40, 42, & 45; project 15 provides the dataset, but it is buried within the code
> repository.)

Noted.

> 4. Can the rubric used for evaluating projects be included in the supplemental materials?

There was no numeric rubric: judges answered Gavel's holistic pairwise question, effectively "which
of these two projects is better?". This is now stated in Hackathon Details and Setup.

> 5. The workflow for transcribing and analyzing the projects is not reproducible at its current
> level of detail. Furthermore, the claim that this approach provides a structured and objective
> assessment of the submissions is not supported by any evidence or reference to prior works.

Addressed: see the rewritten opening of Projects' Key Findings. The objective-assessment claim has
been withdrawn.

### Tables and figures

> 6. Figure 2: The black text which falls above the map can be difficult to read.

Fixed: a thin white outline now surrounds the histogram labels and titles. See Figure 2.

> 7. Table 1 spans two pages but contains no entries on the second page.

Fixed: the project table (now Table III) breaks cleanly with entries on every page.

> 9. Figure 3: The caption contains a statement on preprint server policies which should be updated to
> adhere to Digital Discovery's polices.

Fixed: the caption now states the actual reason for the blurring. See Figure 3.

> 11. Table 2: The "Prize" header is marked for a footnote that is not present.

Fixed: the explanation is folded into the caption and the header carries no marker. The rankings
table is now referenced from the community-judging paragraph in Hackathon Details and Setup and
appears as Table I.

> 13. Figures 4 & 5: Were participants informed that their names and commentary may be made public
> prior to joining the event?

Participant display names are pixelated throughout the keynote room panel in Figure 4, and likewise
in Figure 5.

### Minor comments

> 11. The use of project title headings as links to videos (hosted on YouTube) does not adhere to
> transparent hyperlink standards and is inaccessible on paper copies. In addition, these hyperlinks
> are redundant with the links already provided in Table 1.

Changed to plain text; the links remain in Table III.

> 13a. Project 40 has been migrated from the github listed on its project page to the repo listed in
> the Zenodo metadata file.
> 13b. Projects 33 and 34 do not have github links on their project pages despite having links in the
> Zenodo metadata file.

Fixed on the project pages and in Table III.

> 13. Typographical errors in the Acknowledgement section, around the header for Project 3, and in the
> Author Contributions section. ("Ryan-Rhys Gri ths", "Jakub LÆla", "Can zkan", "Adrian o†i¢",
> "Je rey Watchorn", and potentially others.) Multiple ligatures appear to have been deleted ("fi",
> "ff", etc.).

Fixed: the compiled PDF now embeds glyph-to-Unicode mappings, so these names extract and copy
correctly.

### Data reviewer checklist

Noted; the scripts archived with the manuscript source cover the table generation, summaries,
license tabulation, and figure preparation.
