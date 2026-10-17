"""Generate synthetic healthcare call center transcripts."""

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent.parent / "data" / "synthetic_call_transcripts.csv"

MEMBER_IDS = [f"MBR{str(i).zfill(5)}" for i in range(1, 201)]
AGENTS = [f"Agent_{chr(65 + i)}" for i in range(15)]

CATEGORIES = {
    "billing": [
        "I received a bill that doesn't look right. I was charged ${amount} for a visit that should have been covered. "
        "I already met my deductible this year and I don't understand why I'm being billed again.",
        "My premium went up this month and nobody told me about any changes. I need someone to explain "
        "these charges because this is the third time I've called about billing issues.",
        "I got an EOB that says I owe ${amount} but my doctor's office says I don't owe anything. "
        "Can you help me figure out which one is correct? I'm really frustrated with the back and forth.",
        "I made a payment two weeks ago and it's still not showing on my account. I have the confirmation "
        "number right here. This is unacceptable — I don't want to be sent to collections.",
        "Why was my claim denied? The procedure was pre-authorized and my doctor submitted everything. "
        "I've been on hold for 30 minutes already and I just want this resolved.",
    ],
    "claims": [
        "I submitted a claim three weeks ago and it still shows as pending. My provider said they sent "
        "everything needed. Can you check the status for me?",
        "My claim was denied saying it was out of network, but I specifically verified the provider was "
        "in network before my appointment. I even have a reference number from when I called to check.",
        "I need to file a claim for my emergency room visit last week. I went to the nearest hospital "
        "because it was a real emergency, and I need to make sure it gets processed correctly.",
        "The claim amount doesn't match what my doctor billed. There's a ${amount} difference and I need "
        "to understand the breakdown. My doctor's office is asking me to pay the balance.",
        "I was told my claim would be reprocessed after my appeal, but it's been over a month. "
        "I've called three times about this and each time I'm told to wait. I need this escalated.",
    ],
    "prescription": [
        "My prescription wasn't covered at the pharmacy yesterday. I take this medication every month "
        "and it's always been covered. The pharmacist said something about formulary changes.",
        "I need a prior authorization for my new medication. My doctor faxed the request two days ago "
        "but the pharmacy says they haven't received approval yet. I'm running out of my current supply.",
        "Can you help me find a cheaper alternative to my medication? The copay went up to ${amount} "
        "and I can't afford that every month on my fixed income.",
        "I'm trying to get my prescription transferred to a mail-order pharmacy to save money. "
        "What do I need to do? I've been going back and forth between my pharmacy and your customer service.",
        "The pharmacy says my medication needs a step therapy requirement. I've already tried two other "
        "medications that didn't work. My doctor should be able to override this.",
    ],
    "appointment": [
        "I need help finding a specialist in my network. I've been looking online but the directory "
        "seems outdated — two providers I called aren't accepting new patients.",
        "I want to schedule a wellness visit but I'm not sure what's covered under my preventive care "
        "benefits. I don't want to get a surprise bill afterward.",
        "My doctor referred me to a specialist but they can't see me for three months. Are there other "
        "in-network options that might have earlier availability?",
        "I had a telehealth visit last week and I'm not sure if it was processed correctly. "
        "I want to make sure I'm not going to be charged more than my regular copay.",
        "I'm trying to get a second opinion on a surgery recommendation. Does my plan cover that? "
        "And do I need a referral or can I just go directly?",
    ],
    "general_inquiry": [
        "I just enrolled in my plan and I want to understand my benefits. Can you walk me through "
        "what's covered for mental health services?",
        "I'm moving to a new state next month. What do I need to do to make sure my coverage continues? "
        "Will my current doctors still be in network?",
        "I lost my insurance card and need a replacement. Can you also verify my member ID so I can "
        "go to my appointment tomorrow?",
        "I want to add my newborn to my plan. What documents do I need and what's the deadline? "
        "I don't want to miss the enrollment window.",
        "Can you explain the difference between my in-network and out-of-network benefits? "
        "I want to make sure I'm making the right choices for my family's care.",
    ],
}

SATISFACTION_RESPONSES = {
    "very_dissatisfied": [
        " This has been the worst experience. I want to speak to a supervisor.",
        " I'm going to file a formal complaint. This is unacceptable service.",
        " I've wasted hours on this. Your company needs to do better.",
    ],
    "dissatisfied": [
        " I'm not happy with how this has been handled, but I hope it gets resolved.",
        " This has been frustrating. I expected better service.",
        " I shouldn't have to call multiple times for the same issue.",
    ],
    "neutral": [
        " Okay, I understand. Thank you for explaining that.",
        " Alright, I'll wait for the update. Thanks for your help.",
        "",
    ],
    "satisfied": [
        " Thank you for your help today, I appreciate you taking the time.",
        " That makes sense. I'm glad we could get this sorted out.",
        " Great, that's exactly what I needed. Thank you!",
    ],
}

FRICTION_PHRASES = [
    " I was transferred three times before reaching you.",
    " I've been on hold for over 45 minutes.",
    " This is my fourth call about the same issue.",
    " I already explained this to the last representative.",
    " Nobody seems to know how to fix this problem.",
    " Your automated system kept sending me in circles.",
    " I was disconnected twice before getting through.",
]


def generate_transcript(member_id: str, category: str, is_repeat: bool) -> dict:
    amount = random.choice([50, 75, 120, 200, 350, 500, 850, 1200])
    base_text = random.choice(CATEGORIES[category]).replace("${amount}", str(amount))

    sentiment_weights = (
        {"very_dissatisfied": 0.3, "dissatisfied": 0.4, "neutral": 0.2, "satisfied": 0.1}
        if is_repeat
        else {"very_dissatisfied": 0.05, "dissatisfied": 0.2, "neutral": 0.4, "satisfied": 0.35}
    )
    sentiment = random.choices(
        list(sentiment_weights.keys()), weights=list(sentiment_weights.values()), k=1
    )[0]
    base_text += random.choice(SATISFACTION_RESPONSES[sentiment])

    if is_repeat or random.random() < 0.15:
        base_text += random.choice(FRICTION_PHRASES)

    call_date = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 364))
    duration_minutes = random.randint(3, 35)
    resolved = random.random() < (0.4 if is_repeat else 0.7)

    return {
        "call_id": f"CALL{random.randint(100000, 999999)}",
        "member_id": member_id,
        "call_date": call_date.strftime("%Y-%m-%d"),
        "call_time": f"{random.randint(8, 20):02d}:{random.randint(0, 59):02d}",
        "agent_id": random.choice(AGENTS),
        "category": category,
        "transcript": base_text,
        "duration_minutes": duration_minutes,
        "resolved": resolved,
        "sentiment_label": sentiment,
    }


def main():
    random.seed(42)
    records = []

    repeat_members = random.sample(MEMBER_IDS, 55)

    for member_id in repeat_members:
        n_calls = random.randint(2, 6)
        category = random.choice(list(CATEGORIES.keys()))
        for _ in range(n_calls):
            records.append(generate_transcript(member_id, category, is_repeat=True))

    remaining_members = [m for m in MEMBER_IDS if m not in repeat_members]
    for member_id in remaining_members:
        category = random.choice(list(CATEGORIES.keys()))
        records.append(generate_transcript(member_id, category, is_repeat=False))

    random.shuffle(records)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

    print(f"Generated {len(records)} call transcripts -> {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
