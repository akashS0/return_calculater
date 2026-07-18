import streamlit as st
import plotly.graph_objects as go

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Investment Growth Calculator",
    page_icon="📈",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    /* Main application */

    .stApp {
        background:
        radial-gradient(
            circle at top right,
            rgba(92, 74, 210, 0.18),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #090b14,
            #10121f
        );

        color: white;
    }


    /* Remove Streamlit header */

    header {
        visibility: hidden;
    }


    #MainMenu {
        visibility: hidden;
    }


    footer {
        visibility: hidden;
    }


    /* Main content */

    .block-container {

        max-width: 1250px;

        padding-top: 35px;

        padding-bottom: 60px;

    }


    /* Main title */

    .main-title {

        font-size: 45px;

        font-weight: 800;

        background:
        linear-gradient(
            90deg,
            #ffffff,
            #a995ff
        );

        -webkit-background-clip: text;

        -webkit-text-fill-color: transparent;

        margin-bottom: 5px;

    }


    /* Subtitle */

    .subtitle {

        color: #a7a9bd;

        font-size: 17px;

        margin-bottom: 35px;

    }


    /* Cards */

    .investment-card {

        background:
        linear-gradient(
            145deg,
            rgba(30,32,50,.96),
            rgba(17,19,31,.96)
        );

        border:

        1px solid rgba(
            255,
            255,
            255,
            .09
        );

        border-radius: 24px;

        padding: 28px;

        box-shadow:

        0px 20px 50px

        rgba(
            0,
            0,
            0,
            .30
        );

    }


    /* Metric cards */

    .metric {

        background:

        linear-gradient(
            140deg,
            #1c1e31,
            #131522
        );

        padding: 22px;

        border-radius: 18px;

        border:

        1px solid

        rgba(
            255,
            255,
            255,
            .07
        );

        min-height: 125px;

    }


    /* Metric heading */

    .metric-title {

        color: #9699ae;

        font-size: 14px;

        margin-bottom: 10px;

    }


    /* Metric value */

    .metric-value {

        font-size: 27px;

        font-weight: 750;

        color: white;

    }


    /* Green text */

    .profit {

        color: #1fd5a3;

    }


    /* Input labels */

    label {

        color: #d6d7e4 !important;

        font-weight: 600 !important;

    }


    /* Number input */

    input {

        background:

        #171927 !important;

        color:

        white !important;

        border-radius:

        12px !important;

    }


    /* Select boxes */

    div[data-baseweb="select"] > div {

        background:

        #171927;

        border-radius:

        12px;

    }


    /* Slider */

    .stSlider

    [data-baseweb="slider"]

    div {

        border-radius:

        20px;

    }


    /* Radio buttons */

    div[role="radiogroup"] {

        background:

        #161824;

        padding:

        6px;

        border-radius:

        15px;

    }


    /* Button */

    .stButton button {

        width:

        100%;

        height:

        52px;

        border:

        none;

        border-radius:

        14px;

        background:

        linear-gradient(
            90deg,
            #7357ff,
            #927cff
        );

        color:

        white;

        font-weight:

        700;

        font-size:

        16px;

        transition:

        .25s;

    }


    .stButton button:hover {

        transform:

        translateY(-2px);

        box-shadow:

        0px 10px 25px

        rgba(
            117,
            86,
            255,
            .35
        );

    }


    </style>
    """,

    unsafe_allow_html=True
)


# --------------------------------------------------
# INDIAN CURRENCY FORMAT
# --------------------------------------------------

def indian_currency(amount):

    amount = float(amount)

    if amount >= 10_000_000:

        return (

            f"₹{amount / 10_000_000:,.2f} Cr"

        )

    elif amount >= 100_000:

        return (

            f"₹{amount / 100_000:,.2f} L"

        )

    elif amount >= 1000:

        return (

            f"₹{amount / 1000:,.1f}K"

        )

    else:

        return (

            f"₹{amount:,.0f}"

        )


# --------------------------------------------------
# INVESTMENT CALCULATION
# --------------------------------------------------

def calculate_future_value(

    investment,

    annual_return,

    years,

    frequency

):


    if frequency == "Monthly":

        periods = years * 12

        rate = (

            annual_return

            / 100

            / 12

        )


    else:

        periods = years

        rate = (

            annual_return

            / 100

        )


    # Return is zero

    if rate == 0:

        future_value = (

            investment

            * periods

        )


    else:

        # Investment assumed
        # at beginning of period

        future_value = (

            investment

            *

            (

                (

                    (1 + rate)

                    ** periods

                )

                - 1

            )

            / rate

            *

            (1 + rate)

        )


    total_investment = (

        investment

        * periods

    )


    wealth_gain = (

        future_value

        -

        total_investment

    )


    return (

        total_investment,

        future_value,

        wealth_gain

    )


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.markdown(

    """

    <div class="main-title">

    Investment Growth Calculator

    </div>


    <div class="subtitle">

    See how consistent investing

    can grow your wealth over time.

    </div>

    """,

    unsafe_allow_html=True

)


# --------------------------------------------------
# MAIN COLUMNS
# --------------------------------------------------

left, right = st.columns(

    [0.37, 0.63],

    gap="large"

)


# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------

with left:


    st.markdown(

        """

        <div class="investment-card">

        <h2>

        Investment Details

        </h2>

        """,

        unsafe_allow_html=True

    )


    frequency = st.radio(

        "Investment frequency",

        [

            "Monthly",

            "Yearly"

        ],

        horizontal=True

    )


    investment = st.number_input(

        f"{frequency} investment (₹)",

        min_value=500,

        max_value=10_000_000,

        value=5000,

        step=500

    )


    investment = st.slider(

        "Adjust investment",

        min_value=500,

        max_value=500_000,

        value=int(

            min(

                investment,

                500_000

            )

        ),

        step=500

    )


    annual_return = st.number_input(

        "Expected annual return (%)",

        min_value=0.0,

        max_value=50.0,

        value=12.0,

        step=0.5

    )


    selected_year = st.select_slider(

        "View detailed projection",

        options=[

            10,

            15,

            20,

            25

        ],

        value=10,

        format_func=lambda x:

        f"{x} Years"

    )


    st.button(

        "Calculate Investment Growth"

    )


    st.markdown(

        "</div>",

        unsafe_allow_html=True

    )


# --------------------------------------------------
# CALCULATIONS
# --------------------------------------------------

years_list = [

    10,

    15,

    20,

    25

]


investments = []

future_values = []


for year in years_list:


    invested, future, profit = (

        calculate_future_value(

            investment,

            annual_return,

            year,

            frequency

        )

    )


    investments.append(

        invested

    )


    future_values.append(

        future

    )


# Selected duration

(

    selected_investment,

    selected_future,

    selected_profit

) = calculate_future_value(

    investment,

    annual_return,

    selected_year,

    frequency

)


return_percentage = (

    selected_profit

    /

    selected_investment

    *

    100

)


# --------------------------------------------------
# RESULTS
# --------------------------------------------------

with right:
    st.markdown(
        f"""
        <div class="investment-card">
        <div style="color:#9699ae;font-size:15px;">

        Estimated portfolio value

        after {selected_year} years

        </div>


        <div style="font-size:48px; font-weight:800; margin-top:8px;">

        {indian_currency(selected_future)}

        </div>


        <div style="color:#20d4a3; margin-top:5px;"> + {indian_currency(selected_profit)}

        estimated wealth gained

        </div>


        </div>

        """,

        unsafe_allow_html=True

    )


    st.write("")


    # --------------------------------------------------
    # GRAPH
    # --------------------------------------------------


    figure = go.Figure()


    figure.add_trace(

        go.Bar(

            name=

            "Total Investment",

            x=[

                f"{year}Y"

                for year

                in years_list

            ],

            y=investments,

            marker_color=

            "#514b91",

            hovertemplate=

            "Invested: ₹%{y:,.0f}"

            "<extra></extra>"

        )

    )


    figure.add_trace(

        go.Bar(

            name=

            "Estimated Value",

            x=[

                f"{year}Y"

                for year

                in years_list

            ],

            y=future_values,

            marker_color=

            "#927cff",

            hovertemplate=

            "Portfolio: ₹%{y:,.0f}"

            "<extra></extra>"

        )

    )


    figure.update_layout(

        barmode="group",

        height=430,

        paper_bgcolor=

        "rgba(0,0,0,0)",

        plot_bgcolor=

        "rgba(0,0,0,0)",

        font_color=

        "#a7a9bd",

        margin=dict(

            l=15,

            r=15,

            t=35,

            b=20

        ),

        legend=dict(

            orientation="h",

            y=1.12

        ),

        xaxis=dict(

            title=None,

            showgrid=False

        ),

        yaxis=dict(

            title=None,

            gridcolor=

            "rgba(255,255,255,.06)",

            tickprefix="₹"

        )

    )


    st.plotly_chart(

        figure,

        use_container_width=True,

        config={

            "displayModeBar":

            False

        }

    )


# --------------------------------------------------
# SUMMARY CARDS
# --------------------------------------------------

st.write("")

st.write("")


card1, card2, card3, card4 = st.columns(4)


with card1:


    st.markdown(

        f"""

        <div class="metric">

        <div class="metric-title">

        Total Investment

        </div>

        <div class="metric-value">

        {

        indian_currency(

            selected_investment

        )

        }

        </div>

        </div>

        """,

        unsafe_allow_html=True

    )


with card2:


    st.markdown(

        f"""
        <div class="metric">
        <div class="metric-title">
        Estimated Value
        </div>
        <div class="metric-value">
        {
        indian_currency(
            selected_future
        )
        }
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with card3:


    st.markdown(

        f"""
        <div class="metric">
        <div class="metric-title">
        Wealth Gained
        </div>
        <div class= "metric-value profit">
        {
        indian_currency(
            selected_profit
        )
        }
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with card4:
    st.markdown(

        f"""

        <div class="metric">

        <div class="metric-title">

        Total Return

        </div>

        <div class="metric-value profit">

        +{return_percentage:,.1f}%

        </div>

        </div>

        """,

        unsafe_allow_html=True

    )


# --------------------------------------------------
# DISCLAIMER
# --------------------------------------------------

st.markdown(

    """

    <br>

    <div style="color:#717489;text-align:center;font-size:13px;">

    Calculations are estimates based on a constant expected return. Actual investment returns may vary.

    </div>

    """,
    unsafe_allow_html=True
)
