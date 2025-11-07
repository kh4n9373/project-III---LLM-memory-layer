import os
os.environ["OPENAI_API_KEY"] = "sk-xxx"
os.environ["OPENAI_API_BASE"] = "http://localhost:8001/v1"

# Set your served model name here or via env: SECOM_SEGMENT_MODEL
SEGMENT_MODEL = "Qwen/Qwen3-8B"

from SeCom.secom import SeCom

mm = SeCom(
    granularity="segment",
    config_path="/home/hungpv/projects/memory_data/SeCom/secom/configs/mpnet.yaml",
)

# Override segmentor to use your OpenAI-compatible served model (e.g., Qwen)
# Set disable_reasoning=True to prevent <think> tags in Qwen models
mm.init_segmentor(
    segment_model=SEGMENT_MODEL,
    prompt_path="instructions/segment_with_exchange_number.md",
    incremental_prompt_path="instructions/segment_incremental.md",
    disable_reasoning=True,  # Disable <think> reasoning for Qwen
)

sessions = [
    [
        """
The City and Its Rhythm

Every city has its own heartbeat. You can hear it in the way people walk, how the traffic breathes, and how the lights pulse through the streets at night. Some cities hum like quiet rivers, others roar like the ocean against a steel coast. In this one, mornings begin with chaos — vendors shouting over honking cars, the aroma of coffee and bread escaping into the humid air. The sidewalks feel alive, as if they remember every footstep, every hurried dream that once passed over them. But at dusk, when the sky burns orange and the crowds slow down, the noise folds into something softer. You can almost hear the city sigh.

Sports and Human Energy

There’s something deeply primal about sports — not the medals, not the competition, but the way they remind us that our bodies are built to move. Whether it’s a marathon runner slicing through the cold morning air, or a kid shooting hoops under flickering streetlights, there’s a kind of beauty in motion. In every sprint, every swing, there’s a moment where thought disappears and instinct takes over. It’s in that moment, brief as lightning, that you meet the truest version of yourself — stripped of ego, of fear, of hesitation. The scoreboard might tell one story, but the heartbeat tells another.

Fashion and Expression

Fashion isn’t really about clothes. It’s about translation — taking who you are on the inside and expressing it through fabric, texture, and form. A perfectly fitted suit can feel like armor; a loose vintage shirt might whisper freedom. Streetwear tells one kind of truth, haute couture another, but both speak the same language: identity. You can tell when someone’s wearing something that fits their soul. The confidence in their walk changes; the air around them bends slightly. Maybe fashion isn’t superficial after all — maybe it’s a visual diary of who we are, day by day.

Technology and the Quiet Revolution

We like to think revolutions are loud, but the one we live in now hums quietly behind every screen. Algorithms decide what we see, recommend who we meet, even shape what we believe. Artificial intelligence writes, paints, and reasons; smart devices know our habits better than we do. Yet with all this convenience comes a strange emptiness — a sense that we’ve outsourced part of our humanity to the machines we built. The future isn’t coming; it’s already here, hiding in the pixels. The real challenge isn’t creating smarter technology. It’s remembering to stay human while using it.

Productivity and the Illusion of Progress

We glorify productivity like it’s a moral virtue. To be busy is to be good, to be idle is to be guilty. But what if we’re just running faster on a wheel that doesn’t go anywhere? The to-do list never ends; the inbox always fills again. True progress might not be in doing more, but in learning when to stop. Imagine a culture where rest is seen as strategy, not weakness. Where slowing down isn’t failure, but wisdom. Productivity is useful — but only when it serves purpose, not pride.

The Philosophy of Time

Time is strange. It stretches when you’re bored and disappears when you’re happy. It heals, yet it also steals. Philosophers have wrestled with it for centuries — is time something we move through, or something that moves through us? Some say it’s a straight line, others say it’s a circle. Maybe it’s neither. Maybe time is a mirror, showing us how fragile everything truly is. What’s beautiful about it isn’t that it lasts, but that it doesn’t. Every moment you notice — really notice — becomes infinite for just a second.

Relationships and the Art of Connection

Human connection is the most unpredictable force in the universe. It can lift you higher than success or destroy you faster than failure. We spend years building walls, and then one person walks in and sees through them like glass. Friendship, love, trust — they’re all forms of surrender. You can’t control them; you can only show up. Modern love lives between text bubbles and voice notes, in the glow of screens where feelings are typed instead of spoken. But the truth hasn’t changed: people still crave to be understood more than they crave to be admired.

Nature and the Quiet Reminder

When you step away from the noise — really far away — the world changes its tone. The forest doesn’t hurry. The waves don’t multitask. Mountains don’t compare their heights. Everything just is. The silence isn’t empty; it’s full of presence. It reminds you that peace isn’t something you find; it’s something you return to. The earth doesn’t need saving as much as we need remembering — remembering that we belong to it, not the other way around.

Dreams and the Unwritten Future

At night, when all lights are off and thoughts begin to wander, dreams sneak in — uninvited but necessary. Some dreams are wild, like escape plans from the possible; others are gentle, whispering what our waking minds are too afraid to admit. The future is built first in dreams, then in effort. Every innovation, every love story, every piece of art once started as something invisible. Maybe that’s what keeps us going — the hope that tomorrow can still surprise us.

Epilogue: The Human Thread

Across all these worlds — cities, sports, art, machines, time, and love — one thing ties them together: our desire to make meaning. We build, we run, we dress, we connect, we imagine — not because we have to, but because something inside us refuses to stay still. We are not logical creatures with emotions; we are emotional creatures who learned logic as a survival skill. Maybe that’s the most human thing of all: we keep creating stories, even when we don’t know how they’ll end.
"""
    ],
]
segments = mm.segment(sessions)
print("="*50)
print("FINAL SEGMENTS:")
print("="*50)
print(segments)