document.addEventListener('DOMContentLoaded', () => {
    const jobList = document.getElementById('job-list');
    const actionArea = document.getElementById('action-area');
    const selectedJobInfo = document.getElementById('selected-job-info');
    const startAdventureBtn = document.getElementById('start-adventure-btn');
    const loading = document.getElementById('loading');
    const adventureContent = document.getElementById('adventure-content');
    const jobSelectorSection = document.getElementById('job-selector-section');
    
    let selectedJobId = null;

    // Load Demo Jobs
    fetch('/api/demo/jobs')
        .then(res => res.json())
        .then(res => {
            if (res.success && res.data.length > 0) {
                res.data.forEach(job => {
                    const card = document.createElement('div');
                    card.className = 'job-card';
                    card.innerHTML = `
                        <h4>${job.title}</h4>
                        <p><strong>${job.company_name}</strong></p>
                        <p>${job.location}</p>
                    `;
                    card.onclick = () => {
                        document.querySelectorAll('.job-card').forEach(c => c.classList.remove('selected'));
                        card.classList.add('selected');
                        selectedJobId = job.id;
                        selectedJobInfo.innerText = `已選擇：${job.title} @ ${job.company_name}`;
                        actionArea.classList.remove('hidden');
                    };
                    jobList.appendChild(card);
                });
            } else {
                jobList.innerHTML = '<p>暫無山門開放。</p>';
            }
        });

    // Start Adventure
    startAdventureBtn.onclick = () => {
        if (!selectedJobId) return;
        
        jobSelectorSection.classList.add('hidden');
        loading.classList.remove('hidden');

        fetch('/api/adventure/start', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ job_id: selectedJobId })
        })
        .then(res => res.json())
        .then(res => {
            loading.classList.add('hidden');
            if (res.success) {
                renderAdventure(res.data);
                adventureContent.classList.remove('hidden');
            } else {
                alert(res.message);
                jobSelectorSection.classList.remove('hidden');
            }
        })
        .catch(err => {
            loading.classList.add('hidden');
            alert('修行受阻，請檢查網路連線。');
            jobSelectorSection.classList.remove('hidden');
        });
    };

    function renderAdventure(data) {
        // Vol 1: Strengths
        const strengthsDiv = document.querySelector('#vol-strengths .content');
        strengthsDiv.innerHTML = `
            <p>${data.candidate_strengths.confidence_line}</p>
            ${data.candidate_strengths.strengths.map(s => `
                <div class="strength-item">
                    <span class="item-name">${s.name} <span class="citation-tag">[${s.citation_id}]</span></span>
                    <p>${s.description}</p>
                    <span class="evidence">依據：${s.evidence}</span>
                </div>
            `).join('')}
        `;

        // Vol 2: Job
        const jobDiv = document.querySelector('#vol-job .content');
        jobDiv.innerHTML = `
            <p>${data.job_bright_spots.encouragement}</p>
            ${data.job_bright_spots.bright_spots.map(b => `
                <div class="bright-spot-item">
                    <span class="item-name">${b.name} <span class="citation-tag">[${b.citation_id}]</span></span>
                    <p>${b.description}</p>
                    <span class="evidence">對修行的意義：${b.why_it_matters}</span>
                </div>
            `).join('')}
        `;

        // Vol 3: Story
        const storyDiv = document.querySelector('#vol-story .content');
        storyDiv.innerHTML = `
            <div class="story-text">
                <p><strong>${data.hero_story.hero_title}</strong></p>
                <p>${data.hero_story.opening}</p>
                <p>${data.hero_story.journey_story}</p>
                <p>${data.hero_story.turning_point}</p>
                <p>${data.hero_story.next_chapter}</p>
            </div>
            <p>你的隨身法寶：</p>
            <div class="tools-list">
                ${data.hero_story.three_magic_tools.map(t => `<span class="tool-tag">${t}</span>`).join('')}
            </div>
        `;

        // Vol 4: Quests
        const questsDiv = document.querySelector('#vol-quests .content');
        questsDiv.innerHTML = `
            <p><strong>${data.quest_scroll.quest_title}</strong></p>
            ${data.quest_scroll.quests.map(q => `
                <div class="quest-item">
                    <span class="item-name">Level ${q.level}: ${q.mission}</span>
                    <p>交付物：${q.deliverable}</p>
                    <span class="evidence">信心提升：${q.confidence_boost}</span>
                    <div class="quest-meta">預計耗時：${q.estimated_time}</div>
                </div>
            `).join('')}
            <div class="final-boss-box" style="margin-top: 1.5rem; background: #ffe0b2; padding: 1rem; border-radius: 10px;">
                <p><strong>終極任務：${data.quest_scroll.final_boss.mission}</strong></p>
                <p>"${data.quest_scroll.final_boss.demo_line}"</p>
            </div>
        `;

        // Vol 5: Interview
        const interviewDiv = document.querySelector('#vol-interview .content');
        interviewDiv.innerHTML = `
            <p><strong>關卡：${data.interview_game.stage_name}</strong></p>
            <p>遭遇妖怪：${data.interview_game.monster}</p>
            <p class="story-text" style="font-style: italic;">"${data.interview_game.opening_line}"</p>
            ${data.interview_game.challenges.map(c => `
                <div class="challenge-item">
                    <span class="item-name">試煉：${c.question} <span class="citation-tag">[${c.citation_id}]</span></span>
                    <p>妖怪心思：${c.why_it_matters}</p>
                    <span class="hint">破敵心法：${c.answer_hint}</span>
                    <span class="evidence" style="color: #2e7d32;">信心加持：${c.confidence_boost}</span>
                </div>
            `).join('')}
        `;

        // Final Pack
        const finalDiv = document.querySelector('#vol-final .content');
        finalDiv.innerHTML = `
            <div class="pack-box">
                <p><strong>叩門錦囊 (Application Pack)</strong></p>
                <p><strong>LinkedIn 介紹：</strong><br>${data.application_pack.linkedin_intro}</p>
                <p><strong>自薦信開場：</strong><br>${data.application_pack.cover_letter_opening}</p>
                <p><strong>一分鐘自介：</strong><br>${data.application_pack.elevator_pitch}</p>
                <hr>
                <p style="text-align: center; font-size: 1.2rem; color: var(--primary-color);"><strong>信心咒語：${data.application_pack.confidence_mantra}</strong></p>
            </div>
        `;

        // Citations
        const citationsList = document.getElementById('citations-list');
        citationsList.innerHTML = '';
        data.citations.forEach(cit => {
            const li = document.createElement('li');
            li.innerHTML = `<strong>[${cit.citation_id}]</strong> ${cit.source_name} (${cit.source_type})`;
            citationsList.appendChild(li);
        });
    }
});
