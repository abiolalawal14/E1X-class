# -*- coding: utf-8 -*-
"""
Builds Unsupervised_Learning_Anomaly_Detection_Systems_Beginner_Course.pptx

Run from the project root:
    python build_pptx.py
"""

from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx_helpers import *

V = "visuals/"

prs = new_presentation()

CONTENT_TOP = Inches(1.55)
LEFT_X = Inches(0.78)
FULL_W = Inches(11.78)
COL1_X = Inches(0.78)
COL1_W = Inches(5.55)
COL2_X = Inches(6.60)
COL2_W = Inches(6.00)


def slide_bullets(kicker, title, section, bullets, notes="", subtitle=None, size=17.5, marker="•  "):
    s = blank_slide(prs)
    add_kicker_title(s, kicker, title, section=section)
    top = CONTENT_TOP
    if subtitle:
        add_text(s, LEFT_X, top, FULL_W, Inches(0.5), subtitle, size=16, color=MUTED, italic=True)
        top = Emu(top + Inches(0.55))
    add_bullets(s, LEFT_X, top, FULL_W, Inches(6.95) - top, bullets, size=size, marker=marker)
    if notes:
        add_notes(s, notes)
    return s


def slide_image_right(kicker, title, section, bullets, image, notes="", caption=None,
                       img_width=Inches(5.85), subtitle=None):
    s = blank_slide(prs)
    add_kicker_title(s, kicker, title, section=section)
    top = CONTENT_TOP
    if subtitle:
        add_text(s, COL1_X, top, COL1_W, Inches(0.5), subtitle, size=15.5, color=MUTED, italic=True)
        top = Emu(top + Inches(0.55))
    add_bullets(s, COL1_X, top, COL1_W, Inches(6.9) - top, bullets, size=16.5)
    add_picture_framed(s, V + image, COL2_X, Inches(1.85), w=img_width, caption=caption)
    if notes:
        add_notes(s, notes)
    return s


def slide_image_full(kicker, title, section, image, notes="", caption=None,
                      img_width=Inches(9.4), intro=None, y=Inches(1.75)):
    s = blank_slide(prs)
    add_kicker_title(s, kicker, title, section=section)
    if intro:
        add_text(s, LEFT_X, CONTENT_TOP, FULL_W, Inches(0.5), intro, size=16.5, color=MUTED, italic=True)
        y = Emu(y + Inches(0.35))
    x = Emu(int((SLIDE_W - img_width) / 2))
    add_picture_framed(s, V + image, x, y, w=img_width, caption=caption)
    if notes:
        add_notes(s, notes)
    return s


def slide_flow_v(kicker, title, section, steps, notes="", intro=None, colors=None, box_w=Inches(5.6)):
    s = blank_slide(prs)
    add_kicker_title(s, kicker, title, section=section)
    y = CONTENT_TOP
    if intro:
        add_text(s, LEFT_X, y, FULL_W, Inches(0.5), intro, size=16.5, color=MUTED, italic=True)
        y = Emu(y + Inches(0.5))
    x = Emu(int((SLIDE_W - box_w) / 2))
    n = len(steps)
    box_h = Inches(0.56) if n > 5 else Inches(0.62)
    gap = Inches(0.20) if n > 5 else Inches(0.26)
    if colors is None:
        add_flow_vertical(s, steps, x, y, box_w, box_h=box_h, gap=gap, fill=BLUE)
    else:
        cy = y
        for i, (step, c) in enumerate(zip(steps, colors)):
            add_box_with_text(s, x, cy, box_w, box_h, step, fill=c, radius=0.18, size=15)
            cy = Emu(cy + box_h + gap)
            if i < n - 1:
                cx = Emu(x + box_w // 2)
                add_arrow_between(s, cx, Emu(cy - gap + Pt(2)), cx, Emu(cy - Pt(2)))
    if notes:
        add_notes(s, notes)
    return s


def slide_flow_h(kicker, title, section, steps, notes="", intro=None, colors=None, y=Inches(3.1), h=Inches(1.0)):
    s = blank_slide(prs)
    add_kicker_title(s, kicker, title, section=section)
    if intro:
        add_text(s, LEFT_X, CONTENT_TOP, FULL_W, Inches(0.5), intro, size=16.5, color=MUTED, italic=True)
    add_flow_horizontal(s, steps, LEFT_X, y, FULL_W, h=h, colors=colors)
    if notes:
        add_notes(s, notes)
    return s


def slide_table(kicker, title, section, headers, rows, notes="", intro=None,
                 col_widths=None, table_h=Inches(3.6), header_fill=INK):
    s = blank_slide(prs)
    add_kicker_title(s, kicker, title, section=section)
    top = CONTENT_TOP
    if intro:
        add_text(s, LEFT_X, top, FULL_W, Inches(0.5), intro, size=16, color=MUTED, italic=True)
        top = Emu(top + Inches(0.55))
    add_table(s, LEFT_X, top, FULL_W, table_h, headers, rows, col_widths=col_widths, header_fill=header_fill)
    if notes:
        add_notes(s, notes)
    return s


def slide_code(kicker, title, section, code, bullets=None, notes="", code_h=Inches(2.4), intro=None):
    s = blank_slide(prs)
    add_kicker_title(s, kicker, title, section=section)
    top = CONTENT_TOP
    if intro:
        add_text(s, LEFT_X, top, FULL_W, Inches(0.45), intro, size=16, color=MUTED, italic=True)
        top = Emu(top + Inches(0.5))
    add_code_block(s, LEFT_X, top, FULL_W, code_h, code)
    if bullets:
        bullet_top = Emu(top + code_h + Inches(0.3))
        bullet_h = Emu(int(Inches(6.9)) - int(bullet_top))
        add_bullets(s, LEFT_X, bullet_top, FULL_W, bullet_h, bullets, size=15.5)
    if notes:
        add_notes(s, notes)
    return s


def slide_quote(kicker, title, section, quote, subtext=None, notes="", quote_size=32, fill=DARK_PANEL,
                 text_color=WHITE):
    s = blank_slide(prs)
    add_kicker_title(s, kicker, title, section=section)
    panel = add_rect(s, LEFT_X, Inches(2.1), FULL_W, Inches(3.6), fill=fill, radius=0.06)
    tf = panel.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Pt(30); tf.margin_right = Pt(30)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = quote
    set_font(run, quote_size, text_color, True)
    if subtext:
        p2 = tf.add_paragraph()
        p2.alignment = PP_ALIGN.CENTER
        p2.space_before = Pt(14)
        run2 = p2.add_run()
        run2.text = subtext
        set_font(run2, 17, RGBColor(0xC7, 0xCE, 0xD9), False, True)
    if notes:
        add_notes(s, notes)
    return s


SEC1 = "Section 1 · The Problem"
SEC2 = "Section 2 · Unsupervised Learning"
SEC3 = "Section 3 · How Detection Works"
SEC4 = "Section 4 · Isolation Forest"
SEC5 = "Section 5 · Other Methods"
SEC6 = "Section 6 · Evaluation & Real-World Use"

# ===========================================================================
# SLIDE 1 — TITLE
# ===========================================================================
s = blank_slide(prs, bg=DARK_PANEL)
add_rect(s, Inches(0), Inches(0), Inches(13.333), Inches(0.14), fill=RED)
add_text(s, Inches(0.9), Inches(1.15), Inches(6), Inches(0.4), "BEGINNER DATA SCIENCE SESSION",
          size=14, color=RGBColor(0xFC, 0xA5, 0xA5), bold=True)
add_text(s, Inches(0.9), Inches(2.3), Inches(11.5), Inches(1.3), "Unsupervised Learning", size=48, color=WHITE, bold=True)
add_text(s, Inches(0.9), Inches(3.25), Inches(11.5), Inches(1.1), "Anomaly Detection Systems",
          size=32, color=RGBColor(0xFC, 0xA5, 0xA5), bold=True)
add_rect(s, Inches(0.9), Inches(4.5), Inches(1.3), Pt(3.5), fill=AMBER)
add_text(s, Inches(0.9), Inches(4.7), Inches(10.5), Inches(0.6), "Finding Unusual Patterns When We Don't Have Labels",
          size=19, color=RGBColor(0xE5, 0xE7, 0xEB), italic=True)
for i, (label, c) in enumerate([("No Fraud Labels", RED), ("Learn Normal", BLUE), ("Flag Unusual", AMBER)]):
    add_pill(s, Inches(0.9 + i * 2.55), Inches(6.1), Inches(2.35), Inches(0.5), label, fill=c, text_color=WHITE, size=13)
add_notes(s, "Welcome the class. This is a 2-hour session: Hour 1 is concepts (this deck), Hour 2 is hands-on "
             "Python in the notebooks. Frame it as building ONE thing together — a working fraud-detection system "
             "for a bank — rather than a tour of separate algorithms. Ask: has anyone dealt with fraud, spam, or "
             "quality-control alerts before? Their intuition already knows what 'unusual' means; today we teach a "
             "machine to share that intuition without ever being told what fraud looks like.")

# ===========================================================================
# SLIDE 2 — LEARNING OBJECTIVES
# ===========================================================================
s = blank_slide(prs)
add_kicker_title(s, "Introduction", "By the End of This Session, You Will Be Able To...", section="Slide 2")
objs_left = ["Explain what anomaly detection means.",
             "Explain why anomaly detection can be an unsupervised learning problem.",
             "Distinguish between normal observations and anomalies.",
             "Explain point, contextual, and collective anomalies.",
             "Understand the basic approaches to anomaly detection.",
             "Explain the intuition behind Isolation Forest."]
objs_right = ["Train an Isolation Forest model using Python.",
              "Interpret anomaly predictions and anomaly scores.",
              "Visualize detected anomalies.",
              "Understand false positives and false negatives.",
              "Explain why an anomaly does not automatically mean fraud.",
              "Build a simple anomaly detection workflow, end to end."]
add_bullets(s, COL1_X, CONTENT_TOP, COL1_W, Inches(5.3), objs_left, size=15.5, space_after=12)
add_bullets(s, COL2_X, CONTENT_TOP, COL2_W, Inches(5.3), objs_right, size=15.5, space_after=12)
add_notes(s, "Read through quickly — this is a map learners can check themselves against at the end. Mention "
             "explicitly: nothing here requires advanced math. The goal is that they leave able to build and "
             "explain a working system, not recite formulas.")

# ===========================================================================
# SLIDE 3 — REAL-LIFE SCENARIO
# ===========================================================================
s = blank_slide(prs)
add_kicker_title(s, SEC1, "A Real-Life Scenario", section="Slide 3")
add_table(s, LEFT_X, Inches(1.75), FULL_W, Inches(2.2),
          ["Transaction", "Amount", "Location", "Time"],
          [["1", "₦25,000", "Abuja", "10:05"],
           ["2", "₦30,000", "Abuja", "11:15"],
           ["3", "₦28,000", "Abuja", "13:20"],
           ["4", "₦1,500,000", "Lagos", "13:25"]],
          col_widths=[0.7, 1, 1, 1], header_fill=INK, highlight_col=None)
add_pill(s, Inches(3.4), Inches(4.35), Inches(6.5), Inches(0.65), "Which transaction looks suspicious?",
          fill=RED, text_color=WHITE, size=16)
add_text(s, LEFT_X, Inches(5.35), FULL_W, Inches(1.1),
          "Most people immediately point at Transaction 4 — much larger, different city, minutes after "
          "three small, local transactions. Nobody had to teach you a rule to notice that.", size=15.5,
          color=SUBTEXT, italic=True)
add_notes(s, "Let the class actually answer out loud before revealing anything. Everyone will say "
             "Transaction 4. Ask: 'HOW did you know? Nobody gave you a fraud/not-fraud label for these four "
             "rows.' That question is the entire hook for the session — we're about to teach a machine to do "
             "what they just did instinctively.")

# ===========================================================================
# SLIDE 4 — THE CHALLENGE
# ===========================================================================
s = blank_slide(prs)
add_kicker_title(s, SEC1, "The Challenge", section="Slide 4")
add_text(s, LEFT_X, Inches(1.85), FULL_W, Inches(1.1),
          "What if the bank doesn't have a label telling us which transaction is fraudulent?", size=22,
          color=INK, bold=True)
add_bullets(s, LEFT_X, Inches(3.15), FULL_W, Inches(2.2),
            ["No column says “this transaction is fraud.”", "No historical record of confirmed fraud cases exists yet.",
             "Millions of transactions happen daily — a human can't review them all.",
             "We need the DATA ITSELF to reveal what's unusual."], size=17.5)
add_pill(s, Inches(3.0), Inches(5.7), Inches(7.3), Inches(0.65),
          "This is a classic unlabelled-data problem", fill=BLUE_SOFT, text_color=BLUE_DARK, size=16)
add_notes(s, "This is the pivot into unsupervised learning, though don't use that term yet — let it emerge "
             "naturally in a couple of slides. Key point: in most real fraud systems, labels DO eventually show "
             "up (a customer disputes a charge, an investigator confirms fraud) but they arrive late, are "
             "incomplete, and are expensive to get. So the day-one problem is genuinely unlabelled.")

# ===========================================================================
# SLIDE 5 — WHAT IS AN ANOMALY?
# ===========================================================================
s = blank_slide(prs)
add_kicker_title(s, SEC1, "What Is an Anomaly?", section="Slide 5")
add_text(s, LEFT_X, Inches(1.8), FULL_W, Inches(0.9),
          "“An anomaly is a data point that behaves very differently\nfrom what is normal.”", size=21, color=INK, bold=True)
examples = ["An unusually large transaction", "An unusually frequent login attempt",
            "An unusual spike in server temperature", "Unusual network traffic volume",
            "Unusual credit card activity for a specific customer"]
add_bullets(s, LEFT_X, Inches(3.35), FULL_W, Inches(2.6), examples, size=17)
add_notes(s, "Deliberately give examples OUTSIDE banking too (temperature, network traffic) — this shows anomaly "
             "detection is a general pattern, not a banking-only trick, while we keep using the bank story as our "
             "throughline. Ask: 'can anyone think of an anomaly they've personally noticed in their own life — a "
             "utility bill, a fitness tracker reading, anything?'")

# ===========================================================================
# SLIDE 6 — NORMAL VS ANOMALOUS
# ===========================================================================
slide_image_full(SEC1, "Normal vs. Anomalous", "Slide 6", "01_normal_vs_anomalous.png",
                  intro="Real (synthetic) transaction amounts from our bank dataset — most cluster tightly together.",
                  img_width=Inches(8.6), y=Inches(1.95),
                  notes="Point out the x-axis is log-scaled — without that, the huge outlier transactions would "
                        "squash the whole 'normal' cluster into an unreadable sliver on the left. This is itself "
                        "a useful practical lesson: always LOOK at your data's scale before deciding how to plot "
                        "or model it.")

# ===========================================================================
# SLIDE 7 — SUPERVISED VS UNSUPERVISED
# ===========================================================================
slide_table(SEC2, "Supervised vs. Unsupervised", "Slide 7",
            ["Supervised", "Unsupervised"],
            [["Has labels", "No labels"],
             ["Learns from known outcomes", "Finds patterns"],
             ["Classification", "Clustering / anomaly detection"]],
            col_widths=[1, 1], table_h=Inches(2.6),
            notes="Anchor slide for the whole conceptual half. Explicitly say: anomaly detection is USUALLY "
                  "unsupervised in practice, precisely because confirmed fraud labels are rare, delayed, or "
                  "simply don't exist yet for new kinds of fraud. If labels DO exist and are trustworthy, you'd "
                  "actually prefer plain classification — unsupervised anomaly detection is a fallback for when "
                  "labels are missing, not a universally 'better' choice.")

# ===========================================================================
# SLIDE 8 — HOW DO WE LEARN "NORMAL"?
# ===========================================================================
s = blank_slide(prs)
add_kicker_title(s, SEC2, "How Do We Learn “Normal”?", "Slide 8")
add_text(s, LEFT_X, Inches(1.85), FULL_W, Inches(1.0),
          "If nobody tells the machine what fraud looks like,\nhow can it find fraud?", size=21, color=INK, bold=True)
add_flow_horizontal(s, ["Learn what NORMAL\nlooks like", "Identify observations\nthat don't fit"],
                     Inches(2.4), Inches(3.6), Inches(8.5), h=Inches(1.1), fill=BLUE,
                     colors=[BLUE, AMBER])
add_notes(s, "This reframing is the single most important idea in the whole session: the machine never learns "
             "'fraud' directly — it learns what NORMAL looks like, and flags whatever doesn't match. That's what "
             "makes it unsupervised: no fraud examples are required, only a large pool of (mostly normal) "
             "transactions.")

# ===========================================================================
# SLIDE 9 — DIFFERENT TYPES OF ANOMALIES
# ===========================================================================
s = blank_slide(prs)
add_kicker_title(s, SEC2, "Different Types of Anomalies", "Slide 9")
cards = [("1. Point Anomaly", "A single observation that is unusual all by itself.", BLUE),
         ("2. Contextual Anomaly", "Normal in one context, unusual in another.", AMBER),
         ("3. Collective Anomaly", "A group of observations that's unusual TOGETHER.", TEAL)]
for i, (title, desc, c) in enumerate(cards):
    x = LEFT_X + Inches(i * 4.0)
    add_box_with_text(s, x, Inches(2.1), Inches(3.75), Inches(2.6), f"{title}\n\n{desc}", fill=c,
                       text_color=WHITE, size=15.5, radius=0.08)
add_notes(s, "Preview slide — each type gets its own dedicated example on the next three slides. Beginners often "
             "only think of point anomalies ('one big weird number'); the contextual and collective types are "
             "usually the more surprising, memorable ones, so give them proper room.")

# ===========================================================================
# SLIDE 10 — POINT ANOMALY
# ===========================================================================
slide_image_right(SEC2, "Point Anomaly", "Slide 10",
                   ["Most transactions in our dataset sit between ₦5,000 and ₦500,000.",
                    "One transaction is worth several million naira.",
                    "It's unusual entirely on its own — no other context is needed to spot it.",
                    "This is the easiest kind of anomaly to imagine, but real fraud is often subtler than this."],
                   "02_point_anomaly.png",
                   notes="Keep this one quick — it's the intuitive baseline case everyone already grasps from "
                         "Slide 3. Use it to set up the contrast with the next two slides, which are less obvious.")

# ===========================================================================
# SLIDE 11 — CONTEXTUAL ANOMALY
# ===========================================================================
s = blank_slide(prs)
add_kicker_title(s, SEC2, "Contextual Anomaly", "Slide 11")
add_text(s, LEFT_X, Inches(1.85), FULL_W, Inches(0.9),
          "Something may be normal in one context, but unusual in another.", size=19, color=INK, bold=True)
add_box_with_text(s, LEFT_X, Inches(3.0), Inches(5.6), Inches(2.0),
                   "₦500,000 transaction\n\nNORMAL for a business\ncustomer", fill=TEAL, size=17, radius=0.08)
add_box_with_text(s, Inches(6.85), Inches(3.0), Inches(5.6), Inches(2.0),
                   "₦500,000 transaction\n\nUNUSUAL for a student\naccount", fill=RED, size=17, radius=0.08)
add_text(s, LEFT_X, Inches(5.35), FULL_W, Inches(0.9),
          "Same amount. Same currency. Completely different meaning depending on WHO made the transaction.",
          size=15.5, color=SUBTEXT, italic=True)
add_notes(s, "This is a genuinely important beginner concept — flag it as such explicitly. Common misconception "
             "to pre-empt here: students often assume 'unusual' means a single global threshold applies to "
             "everyone. In practice, good anomaly detection compares each observation to ITS OWN relevant "
             "context (e.g. its customer's own history), not just the whole population.")

# ===========================================================================
# SLIDE 12 — COLLECTIVE ANOMALY
# ===========================================================================
s = blank_slide(prs)
add_kicker_title(s, SEC2, "Collective Anomaly", "Slide 12")
add_box_with_text(s, LEFT_X, Inches(1.9), Inches(5.6), Inches(1.7), "One login attempt\n\nLooks completely normal",
                   fill=TEAL, size=17, radius=0.08)
add_box_with_text(s, Inches(6.85), Inches(1.9), Inches(5.6), Inches(1.7),
                   "500 login attempts\nin 2 minutes\n\nAn unusual PATTERN", fill=RED, size=17, radius=0.08)
add_text(s, LEFT_X, Inches(4.0), FULL_W, Inches(1.3),
          "No single login in that burst is individually suspicious. It's the COMBINATION — many attempts, "
          "tightly clustered in time — that reveals the anomaly. Our own dataset includes a version of this: "
          "a handful of customers with a burst of 15-35 transactions inside one hour.", size=16, color=SUBTEXT)
add_notes(s, "Tie this explicitly back to our synthetic dataset's transaction_frequency feature — that's exactly "
             "how we represent collective anomalies later in the coding session. This is a nice moment to "
             "preview Hour 2 without going into code yet.")

# ===========================================================================
# SLIDE 13 — THE BASIC IDEA
# ===========================================================================
slide_flow_h(SEC3, "The Basic Idea", "Slide 13",
             ["Data", "Learn Normal\nPattern", "Calculate\nUnusualness", "Flag\nAnomalies"],
             colors=[MUTED, BLUE, AMBER, RED], y=Inches(3.2), h=Inches(1.15),
             intro="Every approach we're about to cover follows this same basic shape.",
             notes="This four-box flow is the skeleton the rest of Hour 1 hangs on. Point out that different "
                   "algorithms differ mainly in HOW they do step 2 (learn normal) and step 3 (calculate "
                   "unusualness) — the overall shape stays the same.")

# ===========================================================================
# SLIDE 14 — APPROACHES TO ANOMALY DETECTION
# ===========================================================================
slide_bullets(SEC3, "Approaches to Anomaly Detection", "Slide 14",
              ["Statistical methods — how far is a value from what's typically expected?",
               "Distance-based methods — how far is this point from its neighbours?",
               "Density-based methods — does this point sit in a crowded or a sparse region?",
               "Isolation Forest — how easily can this point be separated from the rest?",
               "One-Class SVM — does this point fall inside or outside the learned boundary of normal data?"],
              notes="Explicitly say: there is no single 'best' way to define unusual — these are five different "
                    "lenses on the same question. We'll go one level deeper on the first three (they build "
                    "intuition), then spend most of our time on Isolation Forest, which is the main algorithm "
                    "for today's hands-on session.")

# ===========================================================================
# SLIDE 15 — STATISTICAL APPROACH
# ===========================================================================
s = blank_slide(prs)
add_kicker_title(s, SEC3, "Statistical Approach", "Slide 15")
add_text(s, LEFT_X, Inches(1.8), FULL_W, Inches(0.55),
          "Illustrative example — one customer's typical transaction behaviour:", size=15.5, color=MUTED, bold=True)
add_table(s, LEFT_X, Inches(2.3), Inches(7.4), Inches(1.7),
          ["Typical mean", "Typical std. deviation", "This transaction"],
          [["₦45,000", "₦15,000", "₦150,000"]], header_fill=INK)
add_code_block(s, LEFT_X, Inches(4.25), Inches(7.4), Inches(0.95),
               "z = (150,000 - 45,000) / 15,000\nz ≈ 7", size=15)
add_text(s, Inches(8.55), Inches(2.35), Inches(3.35), Inches(3.6),
          "A z-score measures how many standard deviations a value sits from the mean.\n\n"
          "z ≈ 7 means this transaction is about 7 standard deviations above what's typical — extremely rare "
          "if this customer's spending followed a normal pattern.", size=14, color=SUBTEXT)
add_notes(s, "Introduce the INTUITION before the formula: 'how many typical steps away from average is this "
             "value?' Then show the formula, then compute it together. Keep this example customer-specific "
             "(their own mean/std) rather than population-wide — this connects back to the contextual anomaly "
             "idea from Slide 11. Limitation to mention briefly: z-scores assume roughly bell-shaped data and "
             "only look at one feature at a time — real transactions have several features at once, which is "
             "exactly why we need more powerful methods.")

# ===========================================================================
# SLIDE 16 — DISTANCE-BASED APPROACH
# ===========================================================================
slide_image_right(SEC3, "Distance-Based Approach", "Slide 16",
                   ["If an observation is far away from most other observations, it may be unusual.",
                    "We measure “far” using distance across all the features together (like we do in K-Means).",
                    "Simple and intuitive — but can struggle when data has many features, or clusters of "
                    "very different sizes."],
                   "03_distance_based.png",
                   notes="If your class already took the K-Means/PCA session, call that out explicitly — this is "
                         "literally the same distance intuition, just used for a different purpose (flagging "
                         "outliers instead of finding groups).")

# ===========================================================================
# SLIDE 17 — DENSITY-BASED APPROACH
# ===========================================================================
slide_image_right(SEC3, "Density-Based Approach", "Slide 17",
                   ["If most observations are packed together and one sits in a very sparse region, "
                    "it may be an anomaly.",
                    "This adapts well when different groups naturally have different densities.",
                    "Local Outlier Factor (LOF) is the classic algorithm built on this idea — "
                    "we'll return to it in Section 5."],
                   "04_density_based.png",
                   notes="Contrast with the previous slide: distance-based methods use a single global notion "
                         "of 'far'; density-based methods adapt locally — a point can be 'close' in absolute "
                         "distance but still unusual if it sits in a region nobody else visits.")

# ===========================================================================
# SLIDE 18 — MEET ISOLATION FOREST
# ===========================================================================
s = blank_slide(prs)
add_kicker_title(s, SEC4, "Meet Isolation Forest", "Slide 18")
add_text(s, LEFT_X, Inches(2.0), FULL_W, Inches(1.3),
          "“Anomalies are easier to isolate than\nnormal observations.”", size=26, color=INK, bold=True)
add_bullets(s, LEFT_X, Inches(3.7), FULL_W, Inches(2.3),
            ["Practical — fast, even on large datasets.", "Widely used in real fraud and intrusion detection systems.",
             "Available directly in scikit-learn.", "Intuitive enough to explain without heavy mathematics.",
             "This is the MAIN algorithm for today's hands-on session."], size=16.5)
add_notes(s, "This is the pivot into the algorithm the rest of the course centres on. State plainly why we chose "
             "it over One-Class SVM or LOF for a first, beginner-friendly session: it needs almost no tuning, "
             "handles multiple features naturally, and its core idea ('easy to isolate = unusual') can be "
             "explained with a picture, not a formula.")

# ===========================================================================
# SLIDE 19 — WHAT DOES "ISOLATION" MEAN?
# ===========================================================================
slide_image_full(SEC4, "What Does “Isolation” Mean?", "Slide 19", "05_isolation_outlier.png",
                  intro="Keep drawing random lines that split the data in half. Watch how quickly the red point gets cut off from everyone else.",
                  img_width=Inches(11.6), y=Inches(2.15),
                  notes="Walk through the three panels left to right. By the very first random split, the "
                        "outlier is already separated from the main group — that's the entire intuition. Ask: "
                        "'if I kept drawing random lines through the crowded blue group, would ANY of them "
                        "separate a single point that quickly?' (Answer: no — see the next slide.)")

# ===========================================================================
# SLIDE 20 — NORMAL POINT VS ANOMALY
# ===========================================================================
slide_image_full(SEC4, "Normal Point vs. Anomaly", "Slide 20", "06_isolation_normal.png",
                  intro="Now watch a NORMAL point (the teal circle, buried inside the crowd) go through the same process.",
                  img_width=Inches(11.6), y=Inches(2.15),
                  notes="Direct visual contrast with the previous slide. After 3 splits, this point is STILL "
                        "boxed in with several neighbours — it took many more cuts and still isn't fully alone. "
                        "Summarize with the key line: normal points need MANY splits to isolate; anomalies need "
                        "very FEW. That split count is essentially the anomaly score.")

# ===========================================================================
# SLIDE 21 — HOW ISOLATION FOREST WORKS
# ===========================================================================
slide_flow_v(SEC4, "How Isolation Forest Works", "Slide 21",
             ["1. Randomly select a feature", "2. Randomly select a split point", "3. Split the data",
              "4. Continue splitting", "5. Observe how quickly each point becomes isolated",
              "6. Repeat many times (many trees)", "7. Calculate anomaly scores"],
             box_w=Inches(6.4),
             notes="This is the central mechanics slide for Isolation Forest — take your time here. Emphasize "
                   "'randomly' twice: unlike a decision tree built to predict a label, these splits have no "
                   "target to optimize for — they're genuinely random, which is exactly what makes the isolation "
                   "signal meaningful.")

# ===========================================================================
# SLIDE 22 — WHY USE MANY TREES?
# ===========================================================================
s = blank_slide(prs)
add_kicker_title(s, SEC4, "Why Use Many Trees?", "Slide 22")
add_text(s, LEFT_X, Inches(1.9), FULL_W, Inches(0.9),
          "“One random tree may give a poor decision.\nMany trees give us a more reliable picture.”",
          size=20, color=INK, bold=True)
add_bullets(s, LEFT_X, Inches(3.3), FULL_W, Inches(2.2),
            ["Isolation Forest builds many independent random trees (an ENSEMBLE).",
             "Each tree gives its own opinion about how easily a point isolates.",
             "The final anomaly score AVERAGES this across all the trees.",
             "This averaging smooths out the luck of any single random tree's split choices."], size=16.5)
add_notes(s, "Analogy: asking one person for a snap judgment vs. averaging the judgment of 100 people — the "
             "average is more stable and less influenced by one person's odd guess. This is the same principle "
             "behind Random Forest, if your class has already seen that.")

# ===========================================================================
# SLIDE 23 — IMPORTANT PARAMETERS
# ===========================================================================
slide_code(SEC4, "Important Parameters", "Slide 23",
           """from sklearn.ensemble import IsolationForest

model = IsolationForest(
    n_estimators=100,
    contamination="auto",
    random_state=42
)""",
           bullets=["n_estimators — how many random trees to build (100 is a solid beginner default).",
                    "contamination — our estimate of what fraction of the data is anomalous.",
                    "random_state — makes the result reproducible.",
                    "We're deliberately NOT covering every available parameter — these three are enough to "
                    "get a working model."],
           code_h=Inches(2.1),
           notes="This exact syntax was verified against the current scikit-learn documentation. Reassure "
                 "beginners: scikit-learn's defaults for n_estimators and max_samples are sensible for most "
                 "problems — contamination is really the only one worth thinking hard about, which is why it "
                 "gets its own slide next.")

# ===========================================================================
# SLIDE 24 — WHAT IS CONTAMINATION?
# ===========================================================================
s = blank_slide(prs)
add_kicker_title(s, SEC4, "What Is Contamination?", "Slide 24")
add_text(s, LEFT_X, Inches(1.85), FULL_W, Inches(0.9),
          "“Contamination is an estimate of how much of the data\nmay be anomalous.”", size=20, color=INK, bold=True)
add_bullets(s, LEFT_X, Inches(3.35), FULL_W, Inches(1.7),
            ["If we set contamination=0.03, we're telling the model: “I expect roughly 3% of transactions to be unusual.”",
             "This directly controls HOW MANY points get flagged — it's essentially a threshold in disguise.",
             "\"auto\" uses a default from the original research paper — a reasonable starting point, not a guarantee."],
            size=16.5)
add_pill(s, Inches(2.6), Inches(5.55), Inches(8.1), Inches(0.65),
          "We'll experiment with different contamination values in Hour 2", fill=AMBER_SOFT, text_color=AMBER, size=15)
add_notes(s, "This slide sets up the Hour 2 mini-challenge directly — flag that explicitly. Common beginner "
             "mistake to pre-empt: contamination is NOT something the model discovers from the data; it's an "
             "ASSUMPTION we feed in, and getting it wrong changes the results a lot (we'll see exact numbers "
             "later: our own dataset goes from 51 flagged transactions at contamination=0.01 to 456 at 'auto').")

# ===========================================================================
# SLIDE 25 — ANOMALY SCORE
# ===========================================================================
slide_image_right(SEC4, "Anomaly Score", "Slide 25",
                   ["Every transaction gets a continuous anomaly score, not just a yes/no flag.",
                    "In scikit-learn's Isolation Forest, LOWER scores mean MORE unusual.",
                    "This lets us rank transactions by how unusual they are — not just sort them into two bins.",
                    "Notice how cleanly the two distributions separate in our own dataset."],
                   "07_anomaly_score_distribution.png",
                   notes="Flag this explicitly as a place where beginners get tripped up: 'higher = more normal' "
                         "is the opposite of what some people expect. Double-check this matches whatever scoring "
                         "function you show in the notebook (score_samples / decision_function) — we verified "
                         "against the current scikit-learn docs that lower values are more anomalous for both.")

# ===========================================================================
# SLIDE 26 — PREDICTION: NORMAL OR ANOMALY?
# ===========================================================================
slide_code(SEC4, "Prediction: Normal or Anomaly?", "Slide 26",
           """>>> model.predict(X)
array([ 1,  1,  1, -1,  1, -1, ...])""",
           bullets=["1  →  normal observation (an “inlier”).",
                    "-1  →  anomaly (an “outlier”).",
                    "predict() converts the continuous anomaly score into this simple yes/no flag, using the "
                    "contamination setting as the cutoff.",
                    "Verified against the current scikit-learn documentation."],
           code_h=Inches(1.4),
           notes="Make the 1 / -1 convention very visually clear — write it big if you're on a whiteboard too. "
                 "This exact convention (1 = normal, -1 = anomaly) is shared across IsolationForest, "
                 "LocalOutlierFactor, and OneClassSVM in scikit-learn, which is a nice consistency to point out.")

# ===========================================================================
# SLIDE 27 — FROM MODEL OUTPUT TO BUSINESS ACTION
# ===========================================================================
s = blank_slide(prs)
add_kicker_title(s, SEC4, "From Model Output to Business Action", "Slide 27")
add_flow_horizontal(s, ["Transaction", "Model", "Anomaly", "Investigation", "Human Decision"],
                     LEFT_X, Inches(1.95), FULL_W, h=Inches(0.95), colors=[MUTED, BLUE, RED, AMBER, TEAL])
add_text(s, LEFT_X, Inches(3.35), FULL_W, Inches(0.6),
          "An anomaly does NOT automatically mean fraud.", size=20, color=RED, bold=True, italic=True)
add_bullets(s, LEFT_X, Inches(4.1), FULL_W, Inches(2.3),
            ["A false positive is a normal transaction wrongly flagged as unusual.",
             "A flagged transaction should trigger investigation, not an automatic block or account freeze.",
             "The model's job is to narrow down WHERE a human should look — not to make the final call."],
            size=16.5)
add_notes(s, "This is one of the most important business-literacy points in the whole session — don't rush it. "
             "Ask: 'what happens to customer trust if the bank blocks every flagged transaction automatically, "
             "and 2 out of 3 of them turn out to be legitimate?' Anomaly detection is a triage tool, not a "
             "verdict.")

# ===========================================================================
# SLIDE 28 — WHEN WOULD WE USE OTHER ALGORITHMS?
# ===========================================================================
slide_table(SEC5, "When Would We Use Other Algorithms?", "Slide 28",
            ["Method", "Basic Idea"],
            [["Isolation Forest", "Easy-to-isolate points are suspicious"],
             ["One-Class SVM", "Learn the boundary of normal data"],
             ["Local Outlier Factor (LOF)", "Identify observations in unusually low-density regions"],
             ["Statistical methods", "Flag observations far from expected behaviour"]],
            col_widths=[1, 1.6], table_h=Inches(3.0),
            notes="Keep this genuinely high-level, as instructed — no deep dive today. If a student asks "
                  "'which is best?', the honest answer is: it depends on the data and the problem, which is "
                  "exactly what the next slide addresses.")

# ===========================================================================
# SLIDE 29 — CHOOSING AN APPROACH
# ===========================================================================
slide_flow_h(SEC5, "Choosing an Approach", "Slide 29",
             ["Start\nSimple", "Understand\nthe Data", "Choose a\nMethod", "Validate\nResults", "Monitor"],
             colors=[BLUE, TEAL, AMBER, PURPLE, RED], y=Inches(3.2), h=Inches(1.15),
             intro="Beginner guidance for picking an approach in practice.",
             notes="This is a practical decision framework students can actually reuse on the job. Emphasize "
                   "'Monitor' at the end — anomaly detection isn't a one-time model you train and forget; "
                   "customer behaviour and fraud patterns both drift over time.")

# ===========================================================================
# SLIDE 30 — HOW DO WE KNOW IT WORKS?
# ===========================================================================
slide_bullets(SEC6, "How Do We Know It Works?", "Slide 30",
              ["Precision — of the transactions we flagged, how many were actually anomalous?",
               "Recall — of the actual anomalies out there, how many did we successfully catch?",
               "False positives — normal transactions wrongly flagged (annoys customers, wastes investigator time).",
               "False negatives — real anomalies we missed entirely (the more dangerous kind of mistake).",
               "Domain / business validation — ultimately, a human investigator's judgment matters too.",
               "Anomaly detection can be HARD to evaluate when true labels aren't available at all — which is "
               "often the whole reason we're using it in the first place."],
              size=16,
              notes="This last bullet is a genuinely important, slightly uncomfortable truth: in a real "
                    "unlabeled setting, you often can't compute precision/recall at all until much later "
                    "(when disputes or investigations eventually confirm ground truth). In our notebooks, we use "
                    "a synthetic dataset WITH known ground truth specifically so you can see these metrics in "
                    "action — make that distinction explicit so students don't assume they'll always have this "
                    "luxury in a real job.")

# ===========================================================================
# SLIDE 31 — FINAL MENTAL MODEL
# ===========================================================================
slide_flow_v(SEC6, "Final Mental Model", "Slide 31",
             ["No labels", "Understand normal behaviour", "Find unusual observations",
              "Calculate anomaly score", "Set / interpret a threshold", "Investigate", "Take business action"],
             box_w=Inches(6.0),
             notes="This is the single-slide summary of the ENTIRE conceptual hour — consider lingering here "
                   "for questions before the coding break. Every slide in Hour 1 maps to one box in this chain.")

# ===========================================================================
# SLIDE 32 — IMPORTANT DISTINCTIONS
# ===========================================================================
slide_table("Instructor Reference", "Important Distinctions", "Slide 32",
            ["Myth", "Reality"],
            [["An anomaly means fraud.", "An anomaly is simply unusual — it may be legitimate, a data error, "
              "fraud, or a new but genuine customer behaviour."],
             ["An outlier should always be removed.", "An outlier may be an error, a legitimate extreme value, "
              "an important event, or fraud — never remove automatically."],
             ["Anomaly detection is the same as classification.", "Classification learns from labelled categories; "
              "anomaly detection identifies unusual behaviour without complete labels."],
             ["Detection = a final decision.", "The model flags something; a human or business process then "
              "decides what action to take."]],
            col_widths=[1, 1.5], table_h=Inches(4.6),
            notes="Consider running this as a rapid true/false check with the class before moving to the quiz — "
                  "these four distinctions are the ones beginners misstate most often in follow-up conversations.")

# ===========================================================================
# SLIDE 33 — QUICK QUIZ
# ===========================================================================
s = blank_slide(prs)
add_kicker_title(s, "Knowledge Check", "Quick Quiz", "Slide 33")
quiz = ["1. What is an anomaly?",
        "2. Why can anomaly detection be an unsupervised learning problem?",
        "3. What does Isolation Forest try to do?",
        "4. What does -1 represent in the Isolation Forest predict() output?",
        "5. Does an anomaly automatically mean fraud?",
        "6. What is the risk of setting the anomaly threshold too aggressively?"]
add_bullets(s, LEFT_X, CONTENT_TOP, FULL_W, Inches(4.5), quiz, size=18, space_after=18, marker="")
add_notes(s, "ANSWER KEY (for instructor use):\n"
             "1. A data point that behaves very differently from what is normal/expected.\n"
             "2. Because we don't need labelled fraud examples — the model learns what NORMAL looks like from "
             "mostly-unlabeled data, then flags whatever doesn't fit; no target column is required.\n"
             "3. It tries to isolate each observation using random splits, and measures how FEW splits it takes "
             "— anomalies isolate quickly, normal points take many more splits.\n"
             "4. -1 means the model has flagged that observation as an anomaly/outlier (1 means normal/inlier).\n"
             "5. No. An anomaly is simply unusual. It could be fraud, a data entry error, or a legitimate but "
             "rare event (e.g. a big genuine purchase). It requires investigation, not an automatic verdict.\n"
             "6. Setting the threshold too aggressively (e.g. a high contamination value, or an overly low score "
             "cutoff) flags too many normal transactions as anomalies — many false positives, wasted "
             "investigation time, and frustrated customers. Too LOOSE a threshold has the opposite risk: missing "
             "real anomalies (false negatives).")

# ===========================================================================
# SLIDE 34 — REFERENCES / SOURCES
# ===========================================================================
s = blank_slide(prs)
add_kicker_title(s, "Appendix", "References / Sources", "Slide 34")
add_text(s, LEFT_X, CONTENT_TOP, FULL_W, Inches(0.32), "Textbook", size=14, color=MUTED, bold=True)
add_bullets(s, LEFT_X, Inches(1.92), FULL_W, Inches(1.05),
            ["Aggarwal, C. C. (2015). Data Mining: The Textbook. Springer. — Chapter 8, “Outlier Analysis” "
             "(extreme value analysis, distance-based and density-based / LOF methods)."],
            size=14.5, space_after=6)
add_text(s, LEFT_X, Inches(2.95), FULL_W, Inches(0.32), "Original Research", size=14, color=MUTED, bold=True)
add_bullets(s, LEFT_X, Inches(3.32), FULL_W, Inches(0.6),
            ["Liu, F. T., Ting, K. M., & Zhou, Z.-H. (2008). Isolation Forest. IEEE ICDM."], size=14.5, space_after=6)
add_text(s, LEFT_X, Inches(4.05), FULL_W, Inches(0.32), "Official Documentation (verified for current syntax)",
          size=14, color=MUTED, bold=True)
add_bullets(s, LEFT_X, Inches(4.42), FULL_W, Inches(1.9),
            ["scikit-learn API Reference — IsolationForest, LocalOutlierFactor, OneClassSVM, StandardScaler "
             "(scikit-learn.org/stable/modules/generated/ ...)",
             "scikit-learn User Guide — Novelty and Outlier Detection "
             "(scikit-learn.org/stable/modules/outlier_detection.html)",
             "Every code snippet in this deck was checked against these pages during development."],
            size=13.5, space_after=8)
add_text(s, LEFT_X, Inches(6.5), FULL_W, Inches(0.32), "Data", size=14, color=MUTED, bold=True)
add_bullets(s, LEFT_X, Inches(6.85), FULL_W, Inches(0.65),
            ["All transaction data used in this course is SYNTHETIC (data/generate_data.py). It does not "
             "represent any real bank, customer, or transaction."], size=12.5, space_after=4)
add_notes(s, "All scikit-learn syntax in this deck (IsolationForest, predict, score_samples, decision_function) "
             "was checked against the official documentation during course development to ensure it reflects "
             "current, non-deprecated APIs.")

# ===========================================================================
# Final pass: footers
# ===========================================================================
total = len(prs.slides)
for i, sl in enumerate(prs.slides, start=1):
    add_footer(sl, i, total, tag="Unsupervised Learning · Anomaly Detection Systems")

prs.save("Unsupervised_Learning_Anomaly_Detection_Systems_Beginner_Course.pptx")
print(f"Saved deck with {total} slides.")
