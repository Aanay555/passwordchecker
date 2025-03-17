# app.py

import streamlit as st

# Custom CSS for animations and styling
st.markdown("""
<style>
    .progress-container {
        width: 100%;
        background-color: #f3f3f3;
        border-radius: 25px;
        overflow: hidden;
        margin: 20px 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    .progress-bar {
        height: 20px;
        transition: all 0.5s ease-in-out;
        background: linear-gradient(45deg, #ff4444, #ffbb33, #00C851);
        background-size: 300% 300%;
        animation: gradientBG 2s ease infinite;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .criteria-list {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    .criteria-item {
        margin: 10px 0;
        font-size: 1.1em;
        display: flex;
        align-items: center;
        gap: 10px;
        transition: all 0.3s ease;
    }

    .criteria-item:hover {
        transform: translateX(10px);
    }

    .strength-display {
        font-size: 1.5em;
        font-weight: bold;
        text-align: center;
        padding: 15px;
        border-radius: 10px;
        margin: 20px 0;
        animation: fadeIn 0.5s ease;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .weak { background-color: #ff444433; color: #ff4444; }
    .moderate { background-color: #ffbb3333; color: #ffbb33; }
    .strong { background-color: #00C85133; color: #00C851; }
</style>
""", unsafe_allow_html=True)

def evaluate_password_strength(password):
    score = 0
    feedback = []
    special_chars = '!@#$%^&*'

    # Length check
    length = len(password) >= 8
    if length:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters long")

    # Uppercase check
    has_upper = any(c.isupper() for c in password)
    if has_upper:
        score += 1
    else:
        feedback.append("Add at least one uppercase letter")

    # Lowercase check
    has_lower = any(c.islower() for c in password)
    if has_lower:
        score += 1
    else:
        feedback.append("Add at least one lowercase letter")

    # Digit check
    has_digit = any(c.isdigit() for c in password)
    if has_digit:
        score += 1
    else:
        feedback.append("Include at least one digit")

    # Special character check
    has_special = any(c in special_chars for c in password)
    if has_special:
        score += 1
    else:
        feedback.append(f"Add a special character ({special_chars})")

    # Determine strength
    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Moderate"
    else:
        strength = "Strong"

    return score, strength, feedback

# Streamlit UI
st.title("🔐 Password Strength Meter")
password = st.text_input("Enter your password:", type="password", placeholder="Type your password...")

if password:
    score, strength, feedback = evaluate_password_strength(password)
    
    # Calculate progress and color
    progress = (score / 5) * 100
    color_map = {
        "Weak": "#ff4444",
        "Moderate": "#ffbb33",
        "Strong": "#00C851"
    }
    
    # Animated progress bar
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-bar" style="width: {progress}%; background-color: {color_map[strength]};"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Strength display
    st.markdown(f"""
    <div class="strength-display {strength.lower()}">
        {strength} Password
    </div>
    """, unsafe_allow_html=True)
    
    # Feedback section
    if strength == "Strong":
        st.balloons()
        st.success("🎉 Excellent! Your password meets all security requirements!")
    else:
        st.warning("🔍 Password Improvement Suggestions:")
        for item in feedback:
            st.markdown(f"⚠️ {item}")
    
    # Criteria checklist
    st.markdown("""
    <div class="criteria-list">
        <h4>Security Criteria:</h4>
    """, unsafe_allow_html=True)
    
    checks = {
        "length": len(password) >= 8,
        "upper": any(c.isupper() for c in password),
        "lower": any(c.islower() for c in password),
        "digit": any(c.isdigit() for c in password),
        "special": any(c in '!@#$%^&*' for c in password)
    }
    
    for label, status in checks.items():
        icon = "✅" if status else "❌"
        text = {
            "length": "At least 8 characters",
            "upper": "Contains uppercase letters",
            "lower": "Contains lowercase letters",
            "digit": "Includes at least one digit",
            "special": f"Has special character (!@#$%^&*)"
        }[label]
        
        st.markdown(f"""
        <div class="criteria-item">
            <span>{icon}</span>
            <span>{text}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

else:
    st.info("🔑 Please enter a password to check its strength")