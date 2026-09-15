import streamlit as st

st.set_page_config(
    page_title="Pension & Investment Planner",
    page_icon="📊",
    layout="wide",
)


# --------------------------------------------------
# STYLES  (navy / blue base, orange accent)
# --------------------------------------------------

st.markdown(
    """
    <style>
    header, #MainMenu, footer { visibility: hidden; }

    .block-container {
        max-width: 1200px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        border-bottom: 2px solid #E2E8F0;
    }
    .stTabs [data-baseweb="tab"] {
        height: 46px;
        padding: 0 18px;
    }
    .stTabs [data-baseweb="tab"] p {
        color: #64748B;
        font-size: 15px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] p { color: #0B2545; }

    /* Section heading inside each tab */
    .section-title {
        color: #0B2545;
        font-size: 22px;
        font-weight: 700;
        margin-top: 8px;
    }
    .section-sub {
        color: #64748B;
        font-size: 14px;
        margin: 2px 0 18px;
    }

    /* Input card */
    [class*="st-key-card_"] {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-top: 4px solid #1D4ED8;
        border-radius: 16px;
        padding: 22px 22px 14px;
        box-shadow: 0 8px 24px rgba(15, 23, 42, .06);
    }
    .card-label {
        color: #1D4ED8;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: .1em;
        text-transform: uppercase;
    }
    label p { color: #334155 !important; font-weight: 600 !important; }
    .amount-words {
        color: #1D4ED8;
        font-size: 13px;
        font-weight: 600;
        margin-top: -8px;
    }

    /* Button */
    .stButton button {
        width: 100%;
        height: 48px;
        border-radius: 10px;
        font-size: 15px;
        font-weight: 700;
        transition: .2s;
    }
    .stButton button:hover {
        background: #EA580C;
        border-color: #EA580C;
        box-shadow: 0 8px 20px rgba(249, 115, 22, .30);
    }

    /* Headline result */
    .hero {
        background: linear-gradient(135deg, #0B2545 0%, #1E40AF 100%);
        border-radius: 18px;
        padding: 28px 30px;
        box-shadow: 0 12px 30px rgba(30, 64, 175, .25);
    }
    .hero-label {
        color: #BFD0EE;
        font-size: 14px;
        font-weight: 600;
    }
    .hero-value {
        color: #FFFFFF;
        font-size: 44px;
        font-weight: 800;
        margin: 6px 0 4px;
    }
    .hero-meta {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 12px;
    }
    .chip {
        background: rgba(255, 255, 255, .12);
        border: 1px solid rgba(255, 255, 255, .20);
        border-radius: 999px;
        color: #FFFFFF;
        font-size: 13px;
        font-weight: 600;
        padding: 5px 12px;
    }
    .chip-orange { background: #F97316; border-color: #F97316; }
    .hero-foot {
        color: #A9BCDD;
        font-size: 12px;
        margin-top: 14px;
    }

    /* Stat cards */
    .stat-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 14px;
        margin-top: 16px;
    }
    .stat {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-top: 3px solid #1D4ED8;
        border-radius: 14px;
        padding: 18px 20px;
    }
    .stat.accent { border-top-color: #F97316; }
    .stat-label {
        color: #64748B;
        font-size: 13px;
        font-weight: 600;
    }
    .stat-value {
        color: #0B2545;
        font-size: 24px;
        font-weight: 800;
        margin-top: 6px;
    }
    .stat.accent .stat-value { color: #EA580C; }

    /* Plan summary */
    .note {
        background: #EFF4FF;
        border: 1px solid #C7D7FE;
        border-radius: 12px;
        color: #1E293B;
        font-size: 14px;
        line-height: 1.6;
        margin-top: 16px;
        padding: 14px 16px;
    }
    .note b { color: #0B2545; }
    .hl { color: #EA580C; font-weight: 700; }

    /* Terms & disclaimer */
    .tnc {
        background: #FFF7ED;
        border: 1px solid #FED7AA;
        border-left: 5px solid #F97316;
        border-radius: 12px;
        margin-top: 32px;
        padding: 18px 22px;
    }
    .tnc-title {
        color: #9A3412;
        font-size: 15px;
        font-weight: 800;
        margin-bottom: 8px;
    }
    .tnc ul {
        color: #334155;
        font-size: 13.5px;
        line-height: 1.65;
        margin: 0;
        padding-left: 18px;
    }

    @media (max-width: 640px) {
        .stat-grid { grid-template-columns: 1fr; }
        .hero-value { font-size: 34px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def render_html(markup):
    # Flatten onto one line so Markdown never mistakes
    # indented HTML for a code block.
    st.markdown(
        " ".join(line.strip() for line in markup.splitlines() if line.strip()),
        unsafe_allow_html=True,
    )


def indian_currency(amount):
    amount = float(amount)
    if amount >= 10_000_000:
        return f"₹{amount / 10_000_000:,.2f} Cr"
    elif amount >= 100_000:
        return f"₹{amount / 100_000:,.2f} L"
    elif amount >= 1000:
        return f"₹{amount / 1000:,.1f}K"
    else:
        return f"₹{amount:,.0f}"


ONES = [
    "", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
    "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen",
    "Seventeen", "Eighteen", "Nineteen",
]
TENS = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]


def number_in_words(n):
    # Indian numbering system: thousand, lakh, crore.
    n = int(n)
    if n == 0:
        return "Zero"
    if n < 20:
        return ONES[n]
    if n < 100:
        return f"{TENS[n // 10]} {ONES[n % 10]}".strip()
    if n < 1000:
        rest = f" {number_in_words(n % 100)}" if n % 100 else ""
        return f"{ONES[n // 100]} Hundred{rest}"
    for divisor, name in [(10_000_000, "Crore"), (100_000, "Lakh"), (1000, "Thousand")]:
        if n >= divisor:
            rest = f" {number_in_words(n % divisor)}" if n % divisor else ""
            return f"{number_in_words(n // divisor)} {name}{rest}"


def amount_in_words(amount):
    render_html(f'<div class="amount-words">{number_in_words(amount)} Rupees</div>')


def calculate_future_value(investment, annual_return, years, frequency):
    if frequency == "Monthly":
        periods = years * 12
        rate = annual_return / 100 / 12
    else:
        periods = years
        rate = annual_return / 100

    if rate == 0:
        future_value = investment * periods
    else:
        # Investment assumed at beginning of period
        future_value = investment * (((1 + rate) ** periods) - 1) / rate * (1 + rate)

    total_investment = investment * periods
    wealth_gain = future_value - total_investment
    return total_investment, future_value, wealth_gain


def projected_corpus(investment, annual_return, years_to_invest, policy_term, frequency):
    # Contributions stop after years_to_invest; the value then keeps
    # compounding annually until the end of the policy term.
    total_investment, investment_value, _ = calculate_future_value(
        investment, annual_return, years_to_invest, frequency
    )
    corpus = investment_value * ((1 + annual_return / 100) ** (policy_term - years_to_invest))
    return total_investment, corpus


def required_investment(goal_amount, annual_return, years_to_invest, period, frequency):
    # Inverse of projected_corpus: what one unit invested per period
    # grows to by the end of the period, scaled up to reach the goal.
    _, value_of_one = projected_corpus(1, annual_return, years_to_invest, period, frequency)
    return goal_amount / value_of_one


# Runs in a same-origin component iframe: captures the visible page
# (the parent document's .block-container) and saves it as PNG or PDF.
DOWNLOAD_WIDGET = """
<style>
    body { margin: 0; font-family: "Source Sans Pro", sans-serif; }
    .bar { display: flex; gap: 8px; justify-content: flex-end; padding: 4px 2px; }
    button {
        background: #FFFFFF;
        border: 1.5px solid #1D4ED8;
        border-radius: 10px;
        color: #1D4ED8;
        cursor: pointer;
        font-size: 14px;
        font-weight: 700;
        height: 40px;
        padding: 0 14px;
        transition: .2s;
    }
    button:hover { background: #F97316; border-color: #F97316; color: #FFFFFF; }
    button:disabled { cursor: wait; opacity: .6; }
</style>
<div class="bar">
    <button id="png">&#11015; Download Image</button>
    <button id="pdf">&#11015; Download PDF</button>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<script>
    const FILENAME = "__FILENAME__";
    const SCALE = 2;
    const HTML2CANVAS_URL = "https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js";
    const host = window.parent;

    // html2canvas must run in the app's own window: a canvas created in this
    // iframe lacks the app's fonts, so words get drawn in a wider fallback
    // font at positions measured with the real one and run together.
    function loadHtml2canvas() {
        if (host.html2canvas) return Promise.resolve();
        return new Promise((resolve, reject) => {
            const script = host.document.createElement("script");
            script.src = HTML2CANVAS_URL;
            script.onload = resolve;
            script.onerror = () => reject(new Error("Could not load html2canvas"));
            host.document.head.appendChild(script);
        });
    }

    async function capturePage() {
        await loadHtml2canvas();
        await host.document.fonts.ready;
        const page = host.document.querySelector(".block-container");
        return host.html2canvas(page, {
            scale: SCALE,
            backgroundColor: "#FFFFFF",
            useCORS: true,
            ignoreElements: (node) => node.tagName === "IFRAME",
            // html2canvas paints a button's background over its label unless
            // the label is positioned; do that in the copy it draws from.
            onclone: (doc) => {
                for (const label of doc.querySelectorAll("button p")) {
                    label.style.position = "relative";
                }
            },
        });
    }

    function saveBlob(blob, name) {
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = name;
        document.body.appendChild(link);
        link.click();
        link.remove();
        setTimeout(() => URL.revokeObjectURL(link.href), 1000);
    }

    async function run(button, save) {
        const label = button.innerHTML;
        button.disabled = true;
        button.innerHTML = "Preparing&hellip;";
        try {
            save(await capturePage());
        } catch (err) {
            console.error(err);
            alert("Sorry, the download could not be created. Please try again.");
        } finally {
            button.disabled = false;
            button.innerHTML = label;
        }
    }

    document.getElementById("png").onclick = (e) => run(e.currentTarget, (canvas) => {
        canvas.toBlob((blob) => saveBlob(blob, FILENAME + ".png"), "image/png");
    });

    document.getElementById("pdf").onclick = (e) => run(e.currentTarget, (canvas) => {
        // One page sized to the captured area, so nothing is cut off.
        const width = canvas.width / SCALE;
        const height = canvas.height / SCALE;
        const pdf = new window.jspdf.jsPDF({
            orientation: width > height ? "landscape" : "portrait",
            unit: "px",
            format: [width, height],
            hotfixes: ["px_scaling"],
        });
        pdf.addImage(canvas.toDataURL("image/png"), "PNG", 0, 0, width, height);
        pdf.save(FILENAME + ".pdf");
    });
</script>
"""


def download_buttons(filename):
    st.iframe(DOWNLOAD_WIDGET.replace("__FILENAME__", filename), height=52)


def section_header(title, subtitle):
    head, actions = st.columns([0.62, 0.38], vertical_alignment="center")
    with head:
        render_html(f"""
            <div class="section-title">{title}</div>
            <div class="section-sub">{subtitle}</div>
        """)
    with actions:
        download_buttons(title.lower().replace(" ", "-"))


def plan_inputs(key_prefix, button_label):
    with st.container(key=f"card_{key_prefix}_inputs"):
        render_html('<div class="card-label">Your plan details</div>')

        frequency = st.radio(
            "Investment Frequency",
            ["Monthly", "Yearly"],
            horizontal=True,
            key=f"{key_prefix}_frequency",
        )

        investment = st.number_input(
            f"{frequency} Investment (₹)",
            min_value=500,
            max_value=10_000_000,
            value=5000,
            step=500,
            key=f"{key_prefix}_investment",
        )
        amount_in_words(investment)

        annual_return = st.number_input(
            "Expected Annual Return (%)",
            min_value=0.0,
            max_value=50.0,
            value=12.0,
            step=0.5,
            key=f"{key_prefix}_return",
        )

        years_to_invest = st.number_input(
            "Years you want to invest in",
            min_value=1,
            max_value=40,
            value=10,
            step=1,
            key=f"{key_prefix}_years",
        )

        policy_term = st.number_input(
            "Policy Term (Years)",
            min_value=years_to_invest + 1,
            max_value=60,
            value=max(25, years_to_invest + 1),
            step=1,
            key=f"{key_prefix}_policy_term",
        )

        st.button(button_label, type="primary", key=f"{key_prefix}_calculate")

    return frequency, investment, annual_return, years_to_invest, policy_term


def result_hero(label, value, chips):
    chip_html = " ".join(f'<span class="chip">{chip}</span>' for chip in chips)
    render_html(f"""
        <div class="hero">
            <div class="hero-label">{label}</div>
            <div class="hero-value">{value}</div>
            <div class="hero-meta">
                <span class="chip chip-orange">Estimate</span>
                {chip_html}
            </div>
            <div class="hero-foot">
                Projected figure based on your inputs. Actual returns may differ.
            </div>
        </div>
    """)


def stat_card(label, value, accent=False):
    css_class = "stat accent" if accent else "stat"
    return (
        f'<div class="{css_class}">'
        f'<div class="stat-label">{label}</div>'
        f'<div class="stat-value">{value}</div>'
        f"</div>"
    )


def disclaimer(include_pension=False):
    pension_line = (
        "<li>Pension figures assume 60% of the corpus is paid as a lump sum and the remaining "
        "40% is converted into a pension at a monthly annuity rate of 0.741%. Actual annuity "
        "rates and policy benefits depend on the insurer and prevailing rates at the time of vesting.</li>"
        if include_pension else ""
    )
    render_html(f"""
        <div class="tnc">
            <div class="tnc-title">Important: Terms &amp; Disclaimer</div>
            <ul>
                <li>All figures shown are <b>estimates for illustration only</b>. They are not
                    guaranteed, and <b>actual returns may differ</b>.</li>
                <li>Calculations assume a constant annual rate of return and contributions made at
                    the start of each period. Real investment returns fluctuate with market conditions.</li>
                {pension_line}
                <li>This calculator does not constitute financial advice. Please read the policy documents
                    carefully and consult a qualified financial advisor before investing.</li>
            </ul>
        </div>
    """)


pension_tab, growth_tab, goal_tab = st.tabs([
    "Pension Plan Calculator",
    "Investment Growth Calculator",
    "I Know My Goal",
])


# --------------------------------------------------
# PENSION PLAN CALCULATOR
# --------------------------------------------------

with pension_tab:

    section_header(
        "Pension Plan Calculator",
        "Estimate your retirement corpus, maturity benefit and monthly pension income.",
    )

    left, right = st.columns([0.38, 0.62], gap="large")

    with left:
        frequency, investment, annual_return, years_to_invest, policy_term = plan_inputs(
            "pension", "Calculate Pension Plan"
        )

    total_investment, corpus_at_maturity = projected_corpus(
        investment, annual_return, years_to_invest, policy_term, frequency
    )

    maturity_amount = corpus_at_maturity * 0.60
    pension_corpus = corpus_at_maturity * 0.40
    monthly_pension = pension_corpus * 0.00741
    annual_pension = monthly_pension * 12

    with right:
        result_hero(
            "Projected Corpus at Maturity",
            indian_currency(corpus_at_maturity),
            [f"Policy term: {policy_term} years", f"Investing for {years_to_invest} years"],
        )

        render_html(
            '<div class="stat-grid">'
            + stat_card("Total Investment", indian_currency(total_investment))
            + stat_card("Maturity Amount (60%)", indian_currency(maturity_amount))
            + stat_card("Monthly Pension", indian_currency(monthly_pension), accent=True)
            + stat_card("Annual Pension", indian_currency(annual_pension), accent=True)
            + "</div>"
        )

        render_html(f"""
            <div class="note">
                <b>Plan summary:</b> If you invest <b>₹{investment:,.0f}</b>
                {"monthly" if frequency == "Monthly" else "annually"}
                for <b>{years_to_invest} years</b> and keep your policy term at
                <b>{policy_term} years</b>, your estimated maturity amount will be
                <span class="hl">{indian_currency(maturity_amount)}</span>
                and your estimated monthly pension will be
                <span class="hl">{indian_currency(monthly_pension)}</span> per month.
            </div>
        """)

    disclaimer(include_pension=True)


# --------------------------------------------------
# INVESTMENT GROWTH CALCULATOR
# --------------------------------------------------

with growth_tab:

    section_header(
        "Investment Growth Calculator",
        "Estimate your projected corpus at the end of your policy term.",
    )

    left, right = st.columns([0.38, 0.62], gap="large")

    with left:
        frequency, investment, annual_return, years_to_invest, policy_term = plan_inputs(
            "growth", "Calculate Investment Growth"
        )

    total_investment, corpus_at_maturity = projected_corpus(
        investment, annual_return, years_to_invest, policy_term, frequency
    )

    with right:
        result_hero(
            "Projected Corpus at Maturity",
            indian_currency(corpus_at_maturity),
            [f"Policy term: {policy_term} years", f"Investing for {years_to_invest} years"],
        )

    disclaimer()


# --------------------------------------------------
# I KNOW MY GOAL
# --------------------------------------------------

with goal_tab:

    section_header(
        "I Know My Goal",
        "Enter your target maturity amount to find out how much you need to invest.",
    )

    left, right = st.columns([0.38, 0.62], gap="large")

    with left:
        with st.container(key="card_goal_inputs"):
            render_html('<div class="card-label">Your goal details</div>')

            goal_frequency = st.radio(
                "Investment Frequency",
                ["Monthly", "Yearly"],
                horizontal=True,
                key="goal_frequency",
            )

            goal_amount = st.number_input(
                "Maturity Amount (₹)",
                min_value=10_000,
                max_value=1_000_000_000,
                value=1_000_000,
                step=10_000,
                key="goal_amount",
            )
            amount_in_words(goal_amount)

            goal_invest_years = st.number_input(
                "Years you want to invest in",
                min_value=1,
                max_value=40,
                value=10,
                step=1,
                key="goal_invest_years",
            )

            goal_years = st.number_input(
                "Period (Years)",
                min_value=goal_invest_years,
                max_value=60,
                value=max(15, goal_invest_years),
                step=1,
                key="goal_years",
            )

            goal_return = st.number_input(
                "Expected Annual Return (%)",
                min_value=0.0,
                max_value=50.0,
                value=12.0,
                step=0.5,
                key="goal_return",
            )

            st.button("Calculate Required Investment", type="primary", key="goal_calculate")

    monthly_needed = required_investment(
        goal_amount, goal_return, goal_invest_years, goal_years, "Monthly"
    )
    yearly_needed = required_investment(
        goal_amount, goal_return, goal_invest_years, goal_years, "Yearly"
    )

    if goal_frequency == "Monthly":
        investment_needed = monthly_needed
        total_invested = monthly_needed * goal_invest_years * 12
    else:
        investment_needed = yearly_needed
        total_invested = yearly_needed * goal_invest_years
    wealth_gain = goal_amount - total_invested

    with right:
        result_hero(
            f"Required {goal_frequency} Investment",
            f"₹{investment_needed:,.0f}",
            [
                f"Goal: {indian_currency(goal_amount)}",
                f"Investing for {goal_invest_years} years",
                f"Period: {goal_years} years",
            ],
        )

        render_html(
            '<div class="stat-grid">'
            + stat_card("Monthly Investment", f"₹{monthly_needed:,.0f}", accent=goal_frequency == "Monthly")
            + stat_card("Yearly Investment", f"₹{yearly_needed:,.0f}", accent=goal_frequency == "Yearly")
            + stat_card("Total Investment", indian_currency(total_invested))
            + stat_card("Wealth Gain", indian_currency(wealth_gain))
            + "</div>"
        )

        render_html(f"""
            <div class="note">
                <b>Plan summary:</b> To reach <b>{indian_currency(goal_amount)}</b> in
                <b>{goal_years} years</b> at an expected return of <b>{goal_return:g}%</b> a year,
                you need to invest about <span class="hl">₹{investment_needed:,.0f}</span>
                {"every month" if goal_frequency == "Monthly" else "every year"}
                for <b>{goal_invest_years} years</b>.
            </div>
        """)

    disclaimer()
