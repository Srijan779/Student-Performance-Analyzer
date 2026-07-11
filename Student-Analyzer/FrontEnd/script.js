document.addEventListener('DOMContentLoaded', () => {
    
    // --- 1. SEARCH LOGIC (index.html) ---
    const searchBtn = document.getElementById('searchBtn');
    if (searchBtn) {
        searchBtn.addEventListener('click', async () => {
            const name = document.getElementById('searchName').value;
            if (!name) {
                alert("Please enter a name to search.");
                return;
            }

            searchBtn.innerText = "Searching...";

            try {
                const response = await fetch(`https://student-performance-backend-xpab.onrender.com/api/search/${name}`);
                if (!response.ok) throw new Error("Student not found");
                
                const data = await response.json();
                
                const searchData = {
                    name: data.name,
                    cgpa: data.cgpa,
                    coding_experience: data.experience,
                    coding_level: data.level,
                    career_goal: data.goal,
                    overall_score: data.score,
                    category: data.category,
                    recommendations: ["Data retrieved successfully from historical database records."]
                };

                localStorage.setItem('studentAnalysis', JSON.stringify(searchData));
                window.location.href = 'result.html';

            } catch (error) {
                alert(`Could not find a student named '${name}' in the database.`);
                searchBtn.innerText = "Search";
            }
        });
    }

    // --- 2. FORM SUBMISSION LOGIC (index.html) ---
    const form = document.getElementById('analyzerForm');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault(); 

            const submitBtn = document.getElementById('submitBtn');
            submitBtn.innerText = "Analyzing...";
            
            const studentData = {
                name: document.getElementById('name').value,
                cgpa: parseFloat(document.getElementById('cgpa').value),
                coding_experience: parseInt(document.getElementById('experience').value),
                coding_level: document.getElementById('level').value,
                career_goal: document.getElementById('goal').value
            };

            try {
                const response = await fetch('https://student-performance-backend-xpab.onrender.com/api/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(studentData)
                });

                if (!response.ok) throw new Error("Server Error");

                const resultData = await response.json();
                const finalRecord = { ...studentData, ...resultData };
                
                localStorage.setItem('studentAnalysis', JSON.stringify(finalRecord));
                window.location.href = 'result.html';

            } catch (error) {
                console.error("Error:", error);
                alert("Failed to connect to backend. Is app.py running?");
                submitBtn.innerText = "Analyze Performance";
            }
        });
    }

    // --- 3. RESULT PAGE LOGIC (result.html) ---
    if (document.getElementById('res-name')) {
        const data = JSON.parse(localStorage.getItem('studentAnalysis'));

        if (!data) {
            window.location.href = 'index.html'; 
            return;
        }

        document.getElementById('res-name').innerText = data.name;
        document.getElementById('res-score').innerText = data.overall_score;
        
        const categoryElement = document.getElementById('res-category');
        categoryElement.innerText = data.category;
        
        // Dynamic coloring based on category
        if (data.category === "Needs Improvement") {
            categoryElement.className = "stat-value text-danger";
            document.getElementById('res-risk').innerText = "High Risk ⚠️";
            document.getElementById('res-risk').className = "stat-value text-danger";
        } else if (data.category === "Average") {
            categoryElement.className = "stat-value";
            categoryElement.style.color = "#fbbf24"; 
            document.getElementById('res-risk').innerText = "Moderate Risk ⚠️";
            document.getElementById('res-risk').style.color = "#fbbf24";
        } else {
            categoryElement.className = "stat-value text-success";
            document.getElementById('res-risk').innerText = "Low Risk ✅";
            document.getElementById('res-risk').className = "stat-value text-success";
        }

        const recList = document.getElementById('res-recs');
        data.recommendations.forEach(rec => {
            let li = document.createElement('li');
            li.innerText = rec;
            recList.appendChild(li);
        });
    }
});
