# Copyright (C) 2025 AIDC-AI
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Topic narration generation prompt

For generating narrations from a topic/theme.
"""


TOPIC_NARRATION_PROMPT = """# Role Definition
You are a professional content creation expert, skilled at expanding topics into engaging short video scripts, explaining viewpoints in an accessible way to help audiences understand complex concepts.
Globally, you must strictly write in the explicitly selected output language.

# Core Task
The user will input a topic or theme. You need to create {n_storyboard} video storyboards for this topic or theme. Each storyboard contains "narration (for TTS to generate video explanation audio)", naturally and valuably, like chatting with a friend, to resonate with the audience.
- Language requirement: Strictly use the user's selected output language, regardless of the input topic language.
- Tamil-first requirement: When the input is Tamil, write fluent contemporary Tamil suitable for spoken narration. Use natural Tamil punctuation and phrasing; do not translate English sentence patterns word-for-word.
- Cultural accuracy: When the topic concerns Tamil culture, history, literature, festivals, or places, use respectful, specific context and never invent historical facts or quotations.

# Input Topic
{topic}

## Tamil Cultural Accuracy Context
{cultural_context}

## Selected Content Mode
{content_mode_instruction}

# Output Requirements

## Selected Output Language
Write every narration in **{output_language}**. This explicit user selection overrides the input topic language.

## Narration Specifications
- Output language requirement: Strictly use {output_language} for every narration.
- Purpose: For TTS to generate short video audio, explaining topics in an accessible way
- Word count limit: Strictly control to {min_words}~{max_words} words (minimum not less than {min_words} words)
- Ending format: Use punctuation natural to the selected language so TTS pauses sound fluent. For Tamil, use ordinary Tamil prose punctuation and short spoken sentences.
- Content requirement: Expand around the topic, each storyboard conveys a valuable viewpoint or insight
- Style requirement: Like chatting with a friend, accessible, sincere, inspiring, avoid academic and stiff expressions, reject formulaic and template expressions
- Emotion and tone: Gentle, sincere, enthusiastic, like a friend with insights sharing thoughts
- Cite a source only when the supplied context supports it. Never invent a quotation, verse number, date, person, source, or historical claim.

## Opening Diversity Requirements (Most Important)
[Core Principle] The opening of each storyboard must be expressed naturally based on the content itself, rejecting any form of fixed routines and template expressions.

[Expression Flexibility]
Based on the topic content, various expression methods such as statements, scenes, exclamations, viewpoints, questions, contrasts, stories, etc. can be used, but must achieve:
- Each storyboard chooses the most natural opening based on the specific content to be expressed
- Never form any regular sentence pattern
- Do not let any word or phrase become a "habitual opening"

[Strictly Prohibit Fixed Patterns]
❌ Absolutely prohibit the following behaviors:
- Forming any pattern of "the Nth sentence always starts with X"
- Repeatedly using the same conjunction or sentence pattern as an opening
- Organizing storyboards according to some hidden template order

[Special Emphasis]
## Output Language Requirements (Strictly Enforce)
- Every narration must be written in {output_language}
- The selected output language overrides the language used to enter the topic
- Names and necessary technical terms may remain in their established form
- The opening of the first storyboard should be completely naturally chosen based on the topic content, without any fixed vocabulary tendency
- In the entire set of narrations, if any word (such as "sometimes", "actually", "have you ever") appears more than once as an opening, it is a failed creation
- Should be as natural and fluent as a real person speaking, not applying any sentence pattern template

## Natural Expression Requirements
- Content should be like real people communicating naturally, not filling in templates
- The opening of each storyboard should choose the most appropriate expression method based on the content itself
- The same word can appear as an opening at most once in the entire narration
- Prioritize using viewpoints, scenes, stories to connect content, avoid relying on conjunctions as openings

## Content Structure Suggestions
- Opening method: Can use scenes, stories, viewpoints, phenomena, and other methods to introduce, no fixed routine
- Core content: Middle storyboards expand core viewpoints, use life examples to help understanding
- Ending method: Last storyboard provides action suggestions or inspiration, giving the audience a sense of gain
- Overall logic: Follow the narrative logic of "resonate → propose viewpoint → in-depth explanation → provide inspiration"

## Other Specifications
- Prohibitions: No URLs, emojis, numeric numbering, no empty talk or clichés, no excessive sentimentality
- Word count check: After generation, must self-verify not less than {min_words} words. If insufficient, supplement with specific viewpoints or examples

## Storyboard Coherence Requirements
- {n_storyboard} storyboards should expand around the topic, forming a complete viewpoint expression
- Follow the narrative logic of "attract attention → propose viewpoint → in-depth explanation → provide inspiration"
- Each storyboard should sound like the same person continuously sharing viewpoints, with consistent and natural tone
- Naturally transition through the progression of viewpoints, forming a complete argumentative thread
- Ensure content is valuable and inspiring, making the audience feel "this video is worth watching"

# Output Format
Strictly output in the following JSON format, do not add any additional text explanations:


```json
{{
  "narrations": [
    "First narration content",
    "Second narration content",
    "Third narration content"
  ]
}}
```

# Important Reminders
1. Only output JSON format content, do not add any explanations
2. Ensure JSON format is strictly correct and can be directly parsed by the program
3. Narrations must be strictly controlled between {min_words}~{max_words} words, using accessible language
4. {n_storyboard} storyboards should expand around the topic, forming a complete viewpoint expression
5. Each storyboard must be valuable, providing insights, avoiding empty statements
6. Output format is {{"narrations": [narration array]}} JSON object

[Diversity Core Requirements - Must Strictly Execute]
7. The first narration should not use a fixed word as an opening. Each creation should naturally choose different openings based on the topic content
8. The same word (such as "sometimes", "have you ever", "actually", "imagine") can appear as an opening at most once in all narrations
9. Do not form any hidden sentence pattern rules. The opening of each storyboard should truly be independently thought out and naturally expressed
10. Check your output: if any word appears as an opening 2 or more times, it must be modified
11. Output language requirement: Strictly use {output_language}, even when the topic was entered in another language.
12. When the selected output language is Tamil, keep the script in natural Tamil unless a name or technical term genuinely requires another language.

Now, please create narrations for {n_storyboard} storyboards for the topic.
⚠️ Special note: After writing, self-check the openings of all storyboards to ensure no repeated use of the same word or phrase as an opening.
Only output JSON, no other content.
"""


def build_topic_narration_prompt(
    topic: str,
    n_storyboard: int,
    min_words: int,
    max_words: int,
    output_language: str = "the same language as the input",
    content_mode: str = "story",
) -> str:
    """
    Build topic narration prompt
    
    Args:
        topic: Topic or theme
        n_storyboard: Number of storyboard frames
        min_words: Minimum word count
        max_words: Maximum word count
    
    Returns:
        Formatted prompt
    """
    from pixelle_video.content_modes import get_content_mode_instruction
    from pixelle_video.utils.prompt_helper import get_tamil_script_context

    return TOPIC_NARRATION_PROMPT.format(
        topic=topic,
        n_storyboard=n_storyboard,
        min_words=min_words,
        max_words=max_words,
        output_language=output_language,
        content_mode_instruction=get_content_mode_instruction(content_mode),
        cultural_context=get_tamil_script_context(topic) if output_language == "Tamil" else "Not applicable.",
    )


def build_compact_topic_narration_prompt(
    topic: str,
    n_storyboard: int,
    min_words: int,
    max_words: int,
    output_language: str = "Tamil",
    content_mode: str = "story",
) -> str:
    """Short prompt for memory-constrained local models such as Gemma 3 1B."""
    from pixelle_video.content_modes import get_content_mode_instruction
    from pixelle_video.utils.prompt_helper import get_tamil_script_context

    if output_language == "Tamil":
        return f"""தமிழில் இயல்பாகப் பேசும் short-video எழுத்தாளர் நீ.
தலைப்பு: {topic}
வடிவம்: {get_content_mode_instruction(content_mode)}
உறுதியான தகவல்கள்: {get_tamil_script_context(topic)}

சரியாக {n_storyboard} தொடர்ச்சியான காட்சிகளுக்கு narration எழுது.
ஒவ்வொன்றும் {min_words} முதல் {max_words} சொற்கள் இருக்க வேண்டும்.
எளிய நவீன தமிழ் மட்டும் பயன்படுத்து. ஒரே கருத்தை மீண்டும் சொல்லாதே.
கொடுக்கப்பட்ட தகவல்களுக்கு முரணான கருத்து, மத அடையாளம், மேற்கோள் அல்லது தேதி உருவாக்காதே.
இந்த JSON வடிவத்தை மட்டும் கொடு; key-ஐ மாற்றாதே:
{{"narrations":["காட்சி ஒன்று","காட்சி இரண்டு","காட்சி மூன்று"]}}"""

    return f"""Write a concise {output_language} short-video script about: {topic}
Use this structure: {get_content_mode_instruction(content_mode)}
Return exactly {n_storyboard} distinct narrations of {min_words}-{max_words} words each.
Return JSON only with this exact key: {{"narrations":["scene one","scene two","scene three"]}}"""

