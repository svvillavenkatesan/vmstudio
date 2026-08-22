# VMStudio — தமிழ் தயாரிப்பு விளக்கக் கையேடு

**தற்போதைய பதிப்பு:** 0.2.0

**தயாரிப்பு நிலை:** செயல்படும் Development / Beta
**முக்கிய நோக்கம்:** தமிழ் creators-க்கான Topic → Script → Visual → Voice → BGM → Final Video workflow

## 1. சுருக்கமான அறிமுகம்

VMStudio ஒரு Tamil-first AI short-video studio. ஒரு தலைப்பு அல்லது தயாரான ஸ்கிரிப்டிலிருந்து காட்சிகளைத் திட்டமிட்டு, AI image/video, தமிழ் narration, subtitles, பின்னணி இசை மற்றும் template layout ஆகியவற்றை இணைத்து இறுதி MP4 வீடியோ உருவாக்குகிறது.

Quick Create-ல் `1 நிமிடம் · 4 காட்சிகள்` preset-ஐத் தேர்ந்தெடுத்தால் நான்கு விரிவான narration scenes உருவாகும். Image template-க்கு `Cinematic zoom / pan` தேர்வு செய்தால் ஒவ்வொரு காட்சியும் அதன் narration audio நேரத்திற்கு மட்டும் தனித்த camera movement-உடன் render செய்யப்பட்டு, பின்னர் வரிசையாக இணைக்கப்படும்.

இது தற்போது செயல்படும் Beta தயாரிப்பு. முழுமையான commercial release என்று கருதக்கூடாது. முக்கிய workflow, Tamil content modes, local draft autosave, prompt review, தமிழ் fonts, templates மற்றும் history உள்ளன. One-click installer, பெரிய அளவிலான hardware compatibility testing, அனைத்து error screens மற்றும் முழுமையான release QA இன்னும் வளர்ச்சிப் பணிகளாகும்.

## 2. தற்போதைய திறன்களின் நிலை

| தேவை | தற்போதைய ஆதரவு | விளக்கம் |
|---|---|---|
| Text / Topic | ஆம் | தமிழ் அல்லது English topic; தயாரான script-யும் வழங்கலாம் |
| Image input | ஆம் | JPG, JPEG, PNG, WebP; சில workflows-ல் GIF |
| Video input | ஆம் | MP4, MOV, AVI, MKV, WebM — தேர்ந்தெடுத்த pipeline-ஐப் பொறுத்தது |
| Audio input | வரையறுக்கப்பட்ட ஆதரவு | Voice reference / cloning workflow அமைந்தால் பயன்படுத்தலாம்; பொதுவான audio-to-video document ingestion இல்லை |
| PDF input | இல்லை | PDF வாசித்து script உருவாக்கும் pipeline தற்போது சேர்க்கப்படவில்லை |
| Tamil script generation | ஆம் | Local Ollama அல்லது OpenAI-compatible LLM மூலம் |
| AI image generation | ஆம் | Local ComfyUI, RunningHub அல்லது supported image API மூலம் |
| AI video / animation | நிபந்தனையுடன் ஆம் | Image-to-video, video workflow அல்லது motion-transfer model தேவையாகும் |
| Tamil voice | ஆம் | ஆண்/பெண் local voice மற்றும் voice-style speed presets; advanced expressive voice workflow சார்ந்தது |
| Subtitles | ஆம் | Final composition layer-ல் Unicode Tamil text; font/style/position controls |
| Existing BGM சேர்த்தல் | ஆம் | MP3, WAV, FLAC, M4A, AAC, OGG library |
| புதிய இசை உருவாக்கம் | இல்லை | Music-generation model/workflow தற்போது இணைக்கப்படவில்லை |
| Real-time web browsing | இல்லை | இணையத்திலிருந்து செய்தி அல்லது facts தானாகத் தேடும் browser/search connector இல்லை |
| Project drafts | ஆம் | Local autosave, reopen, delete; secrets சேமிக்கப்படாது |

## 3. Standalone மற்றும் API சார்பு

VMStudio-வை இரண்டு முறைகளில் இயக்கலாம்.

### Local-first முறை

- Script: Ollama local model
- Image/video: Local ComfyUI மற்றும் கணினியில் நிறுவப்பட்ட models
- Composition: Local templates, FFmpeg மற்றும் fonts
- Draft/history: Local storage

இந்த அமைப்பில் cloud AI API key தேவையில்லை. ஆனால் பயன்படுத்தும் TTS engine அல்லது ComfyUI workflow தனிப்பட்ட model download/இணைய அணுகலைக் கோரலாம். முதல் model download-க்கு இணையம் தேவைப்படலாம். கணினியின் GPU/RAM திறன் generation வேகத்தையும் model தேர்வையும் தீர்மானிக்கும்.

### Cloud / API முறை

OpenAI-compatible LLM, OpenAI image, DashScope/Qwen, ARK/Seedream/Seedance, Kling அல்லது RunningHub போன்ற சேவைகளைத் தேர்ந்தெடுத்தால் அவற்றின் API credentials மற்றும் இணைய இணைப்பு தேவைப்படும். பயன்பாட்டு கட்டணம் அந்தந்த provider-ஐச் சார்ந்தது.

## 4. எழுத்தாக்கம் மற்றும் Tamil Prompt Engine

ஒரு சிறிய topic-இலிருந்து பல காட்சிகளுக்கான script உருவாக்க முடியும். தற்போதைய content modes:

- தமிழ் கதை
- குழந்தைகள் கதை
- தமிழ் கவிதை
- தமிழ் ஹைக்கூ
- தமிழ் பண்பாடு
- தமிழ் வரலாறு
- தமிழ் கல்வி
- செய்திச் சுருக்கம்
- YouTube Shorts
- Instagram Reels
- தயாரிப்பு விளம்பரம்
- ஊக்கமளிக்கும் காணொளி

Tamil Prompt Engine, Pongal, கோலம், மண் பானை, கரும்பு, பாரம்பரிய உடை, கிராமிய தமிழ்நாடு, modern Chennai, செட்டிநாடு, சோழர் காலம், சங்ககாலம், கோவில் மற்றும் கலை போன்ற தேர்ந்தெடுக்கப்பட்ட cultural context-ஐ prompts-ல் சேர்க்கிறது. உருவான script மற்றும் visual prompts பயனரின் ஒப்புதலுக்குப் பிறகே video generation தொடங்கும்.

இலக்கணத் தரம் தேர்ந்தெடுக்கப்பட்ட language model-ஐச் சார்ந்தது. Human review வசதி இருப்பினும் “எப்போதும் பிழையற்றது” என்று உறுதி அளிக்க முடியாது. குறிப்பாக வரலாறு, செய்தி, மருத்துவம் அல்லது சட்டம் சார்ந்த உள்ளடக்கம் வெளியிடும்முன் மனித சரிபார்ப்பு அவசியம்.

## 5. பட உருவாக்கம் மற்றும் Prompt வழங்கும் முறை

பயனர் இரண்டு நிலைகளில் வழிகாட்டலாம்:

1. **Topic:** `தமிழர் பாரம்பரியத்தில் பொங்கல்`
2. **Visual style guide:** `warm cinematic light, authentic rural Tamil Nadu, documentary realism`

VMStudio ஒவ்வொரு narration scene-க்கும் தனி English visual prompt உருவாக்கும். ComfyUI-க்கு அனுப்பும்முன் அதைத் திருத்தி ஒப்புதல் வழங்கலாம்.

நல்ல prompt-ன் அமைப்பு:

`முக்கிய subject + இடம்/காலம் + செயல் + உடை/பொருட்கள் + lighting + camera framing + art style + text-free`

உதாரணம்:

> A Tamil farming family celebrating Pongal in a traditional courtyard, white kolam at the entrance, decorated clay pot boiling over, sugarcane and turmeric leaves, authentic festive clothing, warm sunrise, cinematic documentary realism, vertical composition, no letters, no logo, no watermark.

தமிழ் எழுத்தை AI image-க்குள் உருவாக்கச் சொல்லக்கூடாது. Title மற்றும் subtitles இறுதி composition layer-ல் bundled Tamil fonts மூலம் சேர்க்கப்படும். இதனால் தவறான தமிழ் எழுத்துக்கள் உருவாகும் பிரச்சினை குறையும்.

ஆதரிக்கக்கூடிய பாணிகள் நிறுவப்பட்ட model/workflow-ஐப் பொறுத்து photorealistic, cinematic, illustration, children’s-book, watercolor, historical documentary, product photography, minimal அல்லது social-media visual போன்றவையாக இருக்கலாம்.

UI-யில் 26 இலவச prompt presets உள்ளன: Cinematic Art, Concept Art, Fantasy Art, Dark Fantasy, Anime/Manga, Comic Book, 3D Render, 3D Cartoon, Pixel Art, Low Poly, Matte Painting, Digital Illustration, Editorial Illustration, Children’s Book Illustration, Vintage Poster, Art Nouveau, Art Deco, Steampunk, Cyberpunk, Neon/Futuristic, Paper Cut, Clay/Stop-motion, Woodcut/Linocut, Stained Glass, Collage மற்றும் Mixed Media. இவை software-level prompt presets என்பதால் தனிக் கட்டணம் இல்லை; model license மற்றும் provider usage terms தனியாகப் பொருந்தும்.

## 6. காணொளி மற்றும் Animation

தற்போதைய video வழிகள்:

- AI images-ஐ narration மற்றும் transitions உடன் short video-ஆக அமைத்தல்
- Image-to-video workflow மூலம் still image-க்கு motion உருவாக்குதல்
- Video generation workflow மூலம் AI clips உருவாக்குதல்
- Reference video + image பயன்படுத்தும் motion/action transfer
- Digital-human சார்ந்த workflows

இவை அனைத்தும் ஒரே laptop-ல் உடனடியாக இயங்கும் என்று பொருள் அல்ல. சரியான ComfyUI nodes, checkpoints/models, VRAM மற்றும் workflow compatibility தேவை. Low-VRAM image workflow கிடைக்கிறது; பெரிய video models அதிக hardware வளம் கோரும்.

## 7. குரல், இசை மற்றும் ஒலி

தமிழ் narration-க்கு ஆண் மற்றும் பெண் குரல் தேர்வுகள் உள்ளன. Natural, news, story, poetry, children, calm, motivational போன்ற presets பேசும் வேகத்தை மாற்றுகின்றன. உண்மையான emotion control அல்லது voice cloning-க்கு அதனை ஆதரிக்கும் ComfyUI TTS workflow மற்றும் சட்டபூர்வமான reference voice sample தேவை.

VMStudio தற்போது ஏற்கனவே உள்ள copyright-safe BGM file-ஐத் தேர்வு செய்து preview செய்யவும், narration-க்கு கீழே volume அமைத்து final video-வில் mix செய்யவும் முடியும். புதிய melody அல்லது முழு இசைத்துண்டை AI மூலம் உருவாக்கும் வசதி இன்னும் இல்லை. அதற்கு MusicGen, Stable Audio அல்லது பொருத்தமான API/workflow integration அடுத்த கட்டமாக சேர்க்கப்பட வேண்டும்.

## 8. இணையம் மற்றும் நேரலைத் தகவல்

இணையம் கிடைப்பதால் மட்டும் VMStudio websites-ஐத் தேடி real-time facts சேகரிக்காது. தற்போதைய LLM prompt generation என்பது browser அல்ல. News summary mode-க்கு பயனர் வழங்கும் செய்தி அல்லது குறிப்பையே source ஆகப் பயன்படுத்த வேண்டும்.

எதிர்கால web research module-ல் search provider, source URL capture, date/time, citations, duplicate filtering மற்றும் fact-review screen அவசியம். அது சேர்க்கப்படும்வரை “இன்றைய செய்தி” போன்ற உள்ளடக்கத்தை automatic live data என நம்பக்கூடாது.

## 9. API மற்றும் Automation

தற்போதைய இணைப்பு வகைகள்:

- OpenAI-compatible LLM API: script, title, prompt generation
- Ollama local endpoint: offline/local script generation
- Local ComfyUI: image, video, analysis மற்றும் TTS workflows
- RunningHub: cloud-hosted ComfyUI workflows
- OpenAI image provider
- DashScope/Qwen image, video மற்றும் visual-language services
- ARK / Seedream / Seedance media services
- Kling video service
- VMStudio FastAPI endpoints: content, image/media, TTS, video generation மற்றும் resource listing

இதன் மூலம் topic list batch generation, scheduled content preparation, external desktop/web UI integration, project workflow orchestration, image/video/TTS provider மாற்றுதல் மற்றும் final video pipeline automation செய்யலாம். CSV batch workflow ஒரு திட்டமிட்ட வளர்ச்சி அம்சம்; தற்போதைய UI-யில் newline topic batch உள்ளது.

## 10. முக்கிய பயன்பாடுகள்

- YouTube Shorts மற்றும் Instagram Reels
- தமிழ் கதை மற்றும் குழந்தைகள் கதை
- கவிதை/ஹைக்கூ visual videos
- பள்ளி கல்வி explainers
- தமிழ் பண்பாடு மற்றும் வரலாற்று அறிமுகங்கள்
- உள்ளூர் வணிக/product promotions
- Quote மற்றும் motivational videos
- கோவில்/சுற்றுலா short documentary
- Brand logo, outro மற்றும் contact details சேர்க்கும் branded content — அடுத்த வளர்ச்சி கட்டம்
- பல அளவுகள்: 9:16, 16:9 மற்றும் 1:1 template-ஐப் பொறுத்து

## 11. பொறுப்பான பயன்பாடு

- வரலாறு மற்றும் செய்தி claims-ஐ source-உடன் சரிபார்க்கவும்.
- மற்றொருவரின் குரலை அவருடைய வெளிப்படையான அனுமதியின்றி clone செய்ய வேண்டாம்.
- BGM, images, logos மற்றும் uploaded videos-க்கு உரிமம் இருப்பதை உறுதி செய்யவும்.
- AI output-ஐ வெளியிடும்முன் script, cultural accuracy, subtitles மற்றும் visual continuity-ஐ review செய்யவும்.
- API keys-ஐ GitHub-ல் upload செய்ய வேண்டாம்; local configuration-ல் மட்டும் வைத்திருக்கவும்.

## 12. பரிந்துரைக்கப்பட்ட அடுத்த வளர்ச்சி வரிசை

1. Reusable Brand Kit — logo, channel name, contact details, branded outro
2. PDF/document ingestion மற்றும் source-grounded script creation
3. Real-time web research with citations
4. AI music generation மற்றும் automatic audio ducking
5. Expressive local Tamil TTS / consent-based voice cloning
6. Windows one-click installer, diagnostics மற்றும் release checklist

---

**தீர்மானம்:** தற்போதைய VMStudio தமிழ் short-video உருவாக்கத்திற்கான செயல்படும் Beta engine. Local Ollama + Local ComfyUI அமைப்பில் cloud AI API key இல்லாமல் பெரும்பாலான core workflow-ஐ இயக்க முடியும். ஆனால் முழுமையான offline செயல்பாடு பயன்படுத்தப்படும் voice/model/workflow-ஐச் சார்ந்தது; PDF, live web browsing மற்றும் AI music generation இன்னும் சேர்க்கப்பட வேண்டியவை.
