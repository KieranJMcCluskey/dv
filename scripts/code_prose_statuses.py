#!/usr/bin/env python3
"""
Hand-coded statuses for the 50 NSW rows whose government update is free prose.

These are the 2011-12, 2012-13 and 2013-15 rounds as reported on in the 2015-17
report, which wrote its updates as narrative instead of the labelled "Update:"
field the later reports use. extract_nsw.py deliberately leaves them `unclear`
rather than keyword-matching prose, because doing that produced a false
"implemented" off the phrase "which was completed in 2017" in a paragraph that
also says "no formal response has been received from NSW Health".

Each verdict below was reached by reading the full update. The rule applied,
uniformly:

  implemented  - the words state a specific action was taken or completed
  in progress  - action underway or committed, with no completion stated
  not started  - nothing done, or the approached body never engaged
  rejected     - considered and declined
  superseded   - the government states the recommendation was reframed as another
  unclear      - the words describe adjacent or pre-existing activity without
                 establishing that this ask was acted on

That last category is doing real work and is not a shrug: four rows describe
training or web content that already existed, offered in place of the review,
mandatory unit or module that was actually asked for. Coding those
"implemented" would credit the government for work it did not say it did.

Two rows take their status from another row because the report says so rather
than giving them an update of their own ("See above", "See update above from
FACS in relation to Recommendation 8 of the 2013/15 Report"); both are marked
in `basis`.

What this pass cannot do: these are the GOVERNMENT's accounts of its own
compliance, mostly dated mid-2017, and several are the agency asserting that
pre-existing activity satisfies the ask. A status of "implemented" here means
the agency said it did the thing - not that anyone verified it. The Team's own
verdict on the same recommendations is the five-value split in Table 7.2 of the
2019-21 report, and it is a different measurement.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECS = ROOT / "extracted" / "recommendations"

# id -> (status, decisive quote from the government update, note)
CODED = {
 # ---- 2011-12 round -------------------------------------------------------
 "NSW-2011-2012-1": ("implemented",
   "Recommendation completed and implemented by amendments to the Coroners Act 2009 (NSW) in 2013.",
   "The Team later asked to go further and drop the relationship reference entirely - see related_to."),
 "NSW-2011-2012-2": ("implemented",
   "Recommendation completed and implemented by amendments to the Coroners Act 2009 (NSW) in 2013.", None),
 "NSW-2011-2012-3": ("implemented",
   "Recommendation completed and implemented by amendments to the Coroners Act 2009 (NSW) in 2013.", None),
 "NSW-2011-2012-4": ("implemented",
   "The NSWPF has incorporated this recommendation into our DV SOPs ... such reports were mandated to be "
   "contained in our Intelligence based system within WebCops.",
   "Delivered by a different mechanism than asked: the Event structure in WebCops could not be changed "
   "('difficult and expensive due to the relative antiquity of the base system'), so the requirement was "
   "met through the intelligence system instead."),
 "NSW-2011-2012-5": ("implemented",
   "the DVSAT that was ultimately adopted for operational use statewide in July 1, 2015 ... The DVSAT is "
   "now business as usual for NSWPF",
   "One limb declined: NSWPF was 'unable to implement (f) asking the perpetrator', on the view that the "
   "victim is the more accurate source and the extra question would duplicate."),
 "NSW-2011-2012-6": ("implemented",
   "The current DV SOPs (2012) contain guidelines for police to use when dealing with victims who decline "
   "to make statements or engage with the investigative process.", None),
 "NSW-2011-2012-7": ("implemented",
   "See above.",
   "No update of its own. NSWPF answered recommendations 6 and 7 together - 'The above recommendations are "
   "related and the following responses are provided for both' - so this takes recommendation 6's status."),
 "NSW-2011-2012-9": ("unclear",
   "The Committee developed the Elder Abuse Helpline and Resource Unit which commenced in March 2013.",
   "The ask was that the Ministerial Advisory Committee on Ageing consider using case reviews 8 and 9 of "
   "the Team's report to inform training resources for the helpline. The update confirms the committee met "
   "and the helpline was built, and says nothing about whether the case reviews informed anything."),
 "NSW-2011-2012-10": ("implemented",
   "See update above from FACS in relation to Recommendation 8 of the 2013/15 Report.",
   "No update of its own; takes the status of NSW-2013-2015-8, where Women NSW wrote to the Commonwealth "
   "in January 2016 and the national 'Stop it at the Start' campaign followed."),
 "NSW-2011-2012-11": ("implemented",
   "In January 2016 ANROWS published the Existing knowledge, practice and responses to violence against "
   "women in Australian Indigenous communities ... papers, which examines Indigenous women's experiences of DFV.",
   "Satisfied by pointing to nationally funded ANROWS research rather than a NSW-commissioned study. The "
   "second limb - that the study should inform strategies to support Indigenous victims - is not addressed."),
 "NSW-2011-2012-12": ("superseded",
   "This recommendation was reframed as recommendation 13 of the 2013-2015 Annual Report",
   "The government states the reframing itself. The replacement - convene an interfaith roundtable - was "
   "delivered on 18 July 2017 after 'some delay'. See NSW-2013-2015-13."),
 "NSW-2011-2012-13": ("implemented",
   "The NSW government has written to the Department of Immigration and Citizenship ... We understand that "
   "officers now receive training in relation to how to respond in situations of DFV",
   "The ask was only that NSW encourage the Commonwealth, which it did. The training itself is a federal "
   "matter and the update reports it second-hand ('We understand')."),
 "NSW-2011-2012-14": ("implemented",
   "In 2015, FACS-Housing issued a notice to remind all FACS-Housing staff of their responsibility to "
   "recognise and respond appropriately to clients who present with indicators of domestic and family violence",
   "Notices issued twice, in 2013 and again in 2015."),

 # ---- 2012-13 round -------------------------------------------------------
 "NSW-2012-2013-1": ("unclear",
   "Training delivered to police during the period of the recommendations has evolved in line with changes "
   "to relevant legislation and SOPs at the time ... The sessions are viewed as those most relevant to each "
   "of the recommendations.",
   "The ask was to review and revise recruitment and field training materials. The update maps existing "
   "course sessions onto the recommendation instead, and never says a review or revision took place."),
 "NSW-2012-2013-2": ("rejected",
   "The NSWPF considered developing a mentoring program but ultimately decided not to pursue this option",
   "Declined with reasons: the Regional Coordinators' role and numbers did not suit it, and NSWPF considers "
   "equivalent support already provided through the specialist DVLO role."),
 "NSW-2012-2013-3": ("in progress",
   "This recommendation will be considered by the review. Until the review is completed the NSWPF cannot "
   "adjust the content of the current DVSAT.",
   "Deferred into a DVSAT review run by Justice and Victims Services. NSWPF also flags that any change "
   "'will come at significant expense and difficulty due to required changes to IT, education and training'."),
 "NSW-2012-2013-4": ("implemented",
   "The NSWPF inserted two quick exit buttons to its Internet DV Homepage. The information about deleting "
   "or hiding history has recently been added by way of a hyperlink", None),
 "NSW-2012-2013-5": ("implemented",
   "The NSWPF agreed that where police used a power to detain a person subject to the Mental Health "
   "(Forensic Provisions) Act 1990 (NSW) then a WebCops event record should be created.",
   "The broader limb was declined: NSWPF would not require a record every time an officer merely considered "
   "using a power or discussed bail status, as that would be 'unrealistic (and not operationally viable)'."),
 "NSW-2012-2013-6": ("implemented",
   "The NSWPF DVSOPs mandate the making of appropriate records when responding to or investigating DV "
   "incidents ... The DV Team consistently promote compliance with these DVSOPs in DV forums with DVLOs, "
   "RDVCS and Regional Sponsors", None),
 "NSW-2012-2013-7": ("implemented",
   "The NSWPF Aboriginal Coordination Team conducts 'Policing Aboriginal Communities' courses in 41 Local "
   "Area Commands around the state. This course includes education on kinship and DV ... running since 2012/2013.", None),
 "NSW-2012-2013-8": ("implemented",
   "BAL is now the first point of contact for custody managers in dealing with juvenile offenders with "
   "accommodation issues.",
   "NSWPF states the outcome but disclaims the cause: 'The use of BAL was initiated independently of the "
   "recommendations.'"),
 "NSW-2012-2013-9": ("in progress",
   "Victims Services continues to work with FACS to ensure support under the Victim Support Scheme is "
   "available to victims of crime. This initiative is an ongoing initiative.",
   "The police limb is done - 'The DVSOPs have been updated and information disseminated to relevant "
   "squads' - but the inter-agency coordination and the tailored services for reluctant families remain "
   "ongoing. The Team restated this recommendation in 2015-17; see repeat_of on NSW-2015-2017-33."),
 "NSW-2012-2013-10": ("in progress",
   "The revised NSW Health Domestic and Family Violence Standards and Guidelines are currently being "
   "finalised for stakeholder consultation by PARVAN.", None),
 "NSW-2012-2013-11": ("in progress",
   "The review date for this policy has only just occurred. PARVAN will contact the integrated Care Team to "
   "enact the previous commitment above in July 2017.",
   "The interpreter-training limb is substantially done - ECAV trained roughly 400 interpreters between "
   "2014 and 2017 - while the policy-review limb was still pending at the time of reporting."),
 "NSW-2012-2013-12": ("in progress",
   "Multicultural NSW has been working with NAATI to ensure the accreditation and testing processes for "
   "interpreters require an understanding of the nature and dynamics of family violence.",
   "Stated as work and commitments in train, with no element reported complete."),
 "NSW-2012-2013-13": ("unclear",
   "Multicultural NSW, through the Education Centre Against Violence, conducts up to 8 course every year to "
   "train new and existing interpreters and translators on domestic and family violence issues ... has been "
   "conducting this training for many years",
   "The ask was a mandatory unit inside induction training. The update describes long-standing optional "
   "courses, explicitly pre-dating the recommendation, and does not establish that anything is mandatory "
   "or part of induction."),
 "NSW-2012-2013-14": ("implemented",
   "In December 2016, the Law Society published Guidelines for Contac[t] ... the assessment for Dispute "
   "Resolution in 2016 and Children's Law, Criminal Law and Family Law in 2017 all include domestic and "
   "family violence.", None),
 "NSW-2012-2013-15": ("in progress",
   "because there were no new appointments in 2016 the Judicial Commission was unable to hold a Magistrates "
   "Orientation Program in that year and so the case studies were unable to be trialled ... An Orientation "
   "program will be held in late November 2017.", None),
 "NSW-2012-2013-16": ("not started",
   "NSW Health wrote to the peak body, the Fertility Society of Australia, in 2016 regarding this "
   "recommendation and offering support to implement this recommendation. This offer has not been responded to.",
   "The recommendation was directed at non-government peak bodies, which NSW Health can only invite. A year "
   "on, no reply. One of the clearest dead ends in the dataset."),
 "NSW-2012-2013-17": ("implemented",
   "Women NSW now commissions the Education Centre Against Violence (ECAV) to deliver Tackling Violence ... "
   "the program has expanded into an additional 14 regional locations.", None),
 "NSW-2012-2013-18": ("in progress",
   "Current activit[ies include] development of culturally appropriate and evidence informed parenting "
   "programs for parents with high needs, including targeted trauma-informed parenting programs aimed at "
   "Aboriginal fathers ... will be incorporated in the new TEI program commencing 1 July 2018.", None),
 "NSW-2012-2013-19": ("unclear",
   "No further update.",
   "Supported in the whole-of-government response and then never reported on again. The entire update is "
   "those three words."),
 "NSW-2012-2013-20": ("implemented",
   "Based on the 2012-2013 whole of government response for other agencies listed as lead agencies for this "
   "recommendation, it is confirmed that they have also implemented this recommendation.",
   "NSW Health's own web content was updated, though a dedicated 'domestic violence focussed intranet "
   "portal is currently under construction' and was to launch with the revised Standards and Guidelines."),
 "NSW-2012-2013-21": ("unclear",
   "The Seniors Card website contains a link to the Helpline ... and regularly advertises the Helpline in "
   "e-newsletters, the annual Discount Directory and on the website.",
   "The ask was a module on the Seniors Card website outlining domestic violence information. What exists "
   "is a link to the Elder Abuse Helpline. The substitute may well serve older people, but the thing asked "
   "for was not built."),
 "NSW-2012-2013-22": ("in progress",
   "The Steering Committee for the Prevention of Elder Abuse was reconstituted by the Interdepartmental "
   "Committee on Ageing on 16 June 2017 ... this information will be progressed through that forum.",
   "Four years on, the reporting asked for had not been provided; the committee that was to provide it had "
   "just been reconstituted and was about to meet for the first time."),
 "NSW-2012-2013-23": ("in progress",
   "PARVAN notes that this action is incomplete and that sign off on actioning this item is currently "
   "pending sign off procedures. Action is due to be completed by August 2017.", None),

 # ---- 2013-15 round -------------------------------------------------------
 "NSW-2013-2015-1": ("in progress",
   "The DVDRT Secretariat and the Judicial Commission have committed to holding quarterly meetings in which "
   "the Secretariat will refer judgments and remarks on sentence to the Commission for consideration.",
   "Meetings held through 2016-17 and an article published in July 2017; the standing referral protocol was "
   "committed to rather than reported in place."),
 "NSW-2013-2015-2": ("in progress",
   "the Victim Impact Working Group had been disbanded but ... Victim's Services had recently commenced "
   "working with the Witness Assistance Scheme (ODPP) to revise the current VIS package",
   "The body the Team was told to work with no longer existed. The work was picked up elsewhere, with "
   "Victims Services to seek the Secretariat's feedback 'when it has further progressed'."),
 "NSW-2013-2015-3": ("in progress",
   "the participants identified a range of training, education and awareness raising strategies for ongoing "
   "development and rollout in 2017 and 2018. A follow up roundtable will take place in the first 6 months of 2018.", None),
 "NSW-2013-2015-4": ("in progress",
   "Accordingly component c) of the Recommendation is in progress.",
   "This is the row that keyword-matching coded 'implemented', off the phrase 'which was completed in 2017' "
   "describing one sub-step. The same update opens 'No formal response has been received from NSW Health in "
   "relation to this recommendation', and the parts that advanced were progressed by the Team itself."),
 "NSW-2013-2015-5": ("implemented",
   "The DVDRT Secretariat now has the benefit of regular contact with mental health and drug and alcohol "
   "specialists via the group and can seek information and input from that expert panel to inform the work "
   "of the Team",
   "The mechanism asked for exists in substance, by way of the Team's Manager being appointed to the MHD&A "
   "RCA Classification Group. Worth noting that it was achieved through the Team's own appointments and "
   "that 'no formal response has been received from NSW Health in relation to this recommendation'."),
 "NSW-2013-2015-6": ("in progress",
   "As yet, no mental health specialist has been appointed to the Team and no response has been received "
   "from NSW Health in relation to this recommendation.",
   "Limb (a) satisfied by the appointment of A/Prof Adrian Dunlop in late 2016; limb (b) not done, and the "
   "agency Justice nominated as responsible had not replied."),
 "NSW-2013-2015-7": ("implemented",
   "FACS existing safeguards include mandated quality requirements and the reportable incidents scheme "
   "under the Disability Inclusion Act 2014 (NSW) to ensure appropriate reporting and notifications occur "
   "in relation to incidents of abuse and violence.",
   "The ask was only that ADHC 'give consideration to developing' mandatory internal reporting protocols; "
   "mandated requirements plus forms, guidelines, statewide briefings and Ombudsman training are reported."),
 "NSW-2013-2015-8": ("implemented",
   "Women NSW wrote to the Commonwealth in January 2016 regarding this recommendation. The NSW government "
   "provided support for the National Campaign to Reduce Violence against Women and their Children 'Stop it "
   "at the Start' (launched on 20 April 2016) through the Council of Australian Governments.",
   "The ask was to approach the Commonwealth and suggest the measure be taken up nationally, which is what "
   "is reported. Also supplies the status for NSW-2011-2012-10."),
 "NSW-2013-2015-9": ("implemented",
   "In 2014, the NSWPF DV Team initiated a review of the police response to breach of ADVOs (a copy of "
   "which has been supplied to the DVDRT).", None),
 "NSW-2013-2015-10": ("in progress",
   "the evaluation will go to tender shortly - the evaluation of the DVSAT is planned for 2017/2018.", None),
 "NSW-2013-2015-11": ("implemented",
   "On 3 May 2016, this information bulletin was sent out to the field for circulation to all operational police.",
   "Distributed within the 12 months the recommendation specified. A further update was foreshadowed once "
   "the Residential Tenancies amendments passed."),
 "NSW-2013-2015-13": ("implemented",
   "See below, Recommendation 12 of the Team's 2011/12 Report.",
   "No update of its own. Takes its status from the 2011-12 Recommendation 12 entry, which records that the "
   "Interfaith Roundtable was held at Parliament House on 18 July 2017, attended by the Minister, the State "
   "Coroner and faith leaders, after 'some delay'."),
 "NSW-2013-2015-14": ("not started",
   "Based on a review of the Courts' websites it does not appear that the relevant brochures have been "
   "updated, nor quick close buttons incorporated.",
   "Unusually, a verified negative: Women NSW checked and found nothing had been done. The targets are "
   "federal courts, which NSW can only write to - it had, in March 2016, and would 'contact the Family "
   "Court and the Federal Circuit Court to ask for an update'."),
 "NSW-2013-2015-15": ("implemented",
   "it was agreed that the in addition to continuing to provide the DVDRT Secretariat with copies of its "
   "reports as requested, the NSW Ombudsman will ensure that the DVDRT Secretariat has access to its joint "
   "F[ramework]", None),
}

def main():
    files = sorted(RECS.glob("NSW_*.json"))
    seen, applied = set(), 0
    for f in files:
        rows = json.load(open(f))
        changed = False
        for r in rows:
            if r["id"] not in CODED:
                continue
            seen.add(r["id"])
            if r["status_basis"] != "prose update, not coded":
                raise SystemExit(
                    f"refusing to code {r['id']}: its basis is '{r['status_basis']}', not an "
                    "uncoded prose update. The extraction has changed - re-read it before coding.")
            status, quote, note = CODED[r["id"]]
            r["status"] = status
            r["status_basis"] = "prose update, coded by hand 2026-11-04"
            r["status_quote"] = quote
            r["status_note"] = note
            applied += 1
            changed = True
        if changed:
            f.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    missing = set(CODED) - seen
    if missing:
        raise SystemExit(f"ids in this file that no longer exist in the extraction: {sorted(missing)}")

    # Must cover every uncoded row, or the count is wrong rather than just incomplete.
    left = [r["id"] for f in files for r in json.load(open(f))
            if r["status_basis"] == "prose update, not coded"]
    print(f"coded {applied} rows; prose rows still uncoded: {left or 'none'}")

    from collections import Counter
    print("verdicts:", dict(Counter(v[0] for v in CODED.values())))

if __name__ == "__main__":
    main()
