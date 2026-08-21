# VILLVA MEDIA STUDIO

தமிழில் short video உருவாக்குவதற்கான AI video studio.

## இது என்ன செய்கிறது

`தலைப்பு → தமிழ் script → காட்சிகள் → குரல் → இசை → final video`

- Tamil-first web interface
- முழு UI-க்கு தமிழ் அல்லது English தேர்வு; video narration-க்கு தனியான தமிழ் அல்லது English தேர்வு
- தமிழ் பண்பாடு, கதை, கல்வி, கவிதை ஆகியவற்றுக்கான 9:16 templates
- தமிழ் ஆண் மற்றும் பெண் Edge TTS voices
- Pongal, Tamil culture, temple, Tamil literature, Sangam/Chola history போன்ற தலைப்புகளுக்கான cultural visual context
- AI-generated image-இல் எழுத்து உருவாக்காமல், final composition layer-ல் Unicode Tamil text overlay
- Local ComfyUI, RunningHub, அல்லது supported image/video API providers மூலம் media generation

## தொடங்குவது

Windows-ல் `VILLVA_MEDIA_STUDIO.bat`-ஐ double-click செய்யுங்கள்.

முதல் முறையில்:

1. `uv` மற்றும் project dependencies இருக்க வேண்டும். இல்லை என்றால் project folder-ல் `uv sync` இயக்கவும்.
2. Web UI-ல் LLM API settings-ஐ நிரப்பி Save செய்யவும்.
3. உள்ளக ComfyUI பயன்படுத்தினால் அதை முதலில் தொடங்கவும்; இயல்புநிலை முகவரி `http://127.0.0.1:8188`.
4. முதலில் `📝 தமிழ் கவிதை` போன்ற static template-ல் test செய்யவும். இதற்கு image model தேவையில்லை.
5. பிறகு `🪔 தமிழ் பண்பாடு` அல்லது `🎬 தமிழ் கதை` template தேர்ந்தெடுத்து AI image workflow அமைக்கவும்.

## Tamil text policy

AI image models-க்கு Tamil letters, title, subtitles, banners அல்லது watermark உருவாக்கச் சொல்லப்படாது. அவை தவறாக வரும் வாய்ப்பு அதிகம். VILLVA templates title மற்றும் narration-ஐ HTML composition layer-ல் render செய்கின்றன.

## வெளிப்புற தேவைகள்

- LLM API key: தமிழ் தலைப்பிலிருந்து script உருவாக்க
- Image/video provider அல்லது ComfyUI: dynamic visuals உருவாக்க
- ComfyUI workflow பயன்படுத்தினால் அதற்கு தேவையான models மற்றும் custom nodes
- FFmpeg மற்றும் Chromium/Playwright: final video composition

இந்த source tree-ல் API keys சேர்க்கப்படவில்லை. அவை local `config.yaml`-ல் மட்டும் சேமிக்கப்படும்; அதை Git-ல் commit செய்யக்கூடாது.
