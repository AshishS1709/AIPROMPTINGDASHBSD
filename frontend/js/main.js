// Show/hide festival section based on content category
document.getElementById('content-category').addEventListener('change', (e) => {
    const festivalSection = document.getElementById('festival-section');
    if (e.target.value === 'Festival / Occasion') {
        festivalSection.classList.remove('hidden');
    } else {
        festivalSection.classList.add('hidden');
    }
});

document.getElementById('generator-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const submitBtn = document.getElementById('generate-btn');
    const btnText = submitBtn.querySelector('.btn-text');
    const spinner = submitBtn.querySelector('.spinner');
    const welcomeState = document.getElementById('welcome-state');
    const resultStage = document.getElementById('result-stage');

    // UI Feedback
    btnText.textContent = 'Generating...';
    spinner.classList.remove('hidden');
    submitBtn.disabled = true;

    const contentCategory = document.getElementById('content-category').value;

    const payload = {
        profile: {
            name: document.getElementById('brand-name').value,
            industry: document.getElementById('industry').value,
            primary_service: document.getElementById('primary-service').value,
            target_audience: document.getElementById('target-audience').value,
            tone: document.getElementById('brand-tone').value,
            phone: document.getElementById('brand-phone').value,
            cta: document.getElementById('cta').value,
            forbidden_words: []
        },
        brief: {
            platform: document.getElementById('platform').value,
            content_category: contentCategory,
            topic: document.getElementById('topic').value,
            festival_name: contentCategory === 'Festival / Occasion' ? document.getElementById('festival-name').value : null,
            festival_type: contentCategory === 'Festival / Occasion' ? document.getElementById('festival-type').value : null,
            cta_enabled: contentCategory === 'Festival / Occasion' ? document.getElementById('cta-enabled').value === 'true' : false
        }
    };

    try {
        const response = await fetch('/generate-post', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error('Generation failed');

        const data = await response.json();
        renderResult(data, payload.profile.name);

        welcomeState.classList.add('hidden');
        resultStage.classList.remove('hidden');
    } catch (error) {
        console.error(error);
        alert('Error generating post. Please check the console and ensure the server is running.');
    } finally {
        btnText.textContent = 'Generate Post';
        spinner.classList.add('hidden');
        submitBtn.disabled = false;
    }
});

function renderResult(data, brandName) {
    document.getElementById('preview-brand-name').textContent = brandName;

    // Update Avatar Initials
    const initials = brandName.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
    document.getElementById('preview-avatar').textContent = initials;

    document.getElementById('res-headline').textContent = data.headline;
    document.getElementById('res-caption').textContent = data.caption;
    document.getElementById('res-cta').textContent = data.cta;
    document.getElementById('res-design-prompt').textContent = data.design_prompt;

    // Render Hashtags
    const tagsContainer = document.getElementById('res-hashtags');
    tagsContainer.innerHTML = data.hashtags.map(tag => `<span>#${tag.replace('#', '')}</span>`).join(' ');

    // Render Image (Hide if not present)
    const imageContainer = document.getElementById('preview-image');
    if (data.image_url) {
        imageContainer.classList.remove('hidden');
        // Convert local path to web URL (served by static mount)
        // Backend returns: output\\filename.png
        // Static URL is: http://127.0.0.1:8000/output/filename.png
        const filename = data.image_url.split(/[\\\/]/).pop();
        const webUrl = `/output/${filename}`;

        imageContainer.innerHTML = `<img src="${webUrl}" alt="Generated Content" class="post-image">`;
    } else {
        imageContainer.classList.add('hidden');
        imageContainer.innerHTML = '';
    }
}

