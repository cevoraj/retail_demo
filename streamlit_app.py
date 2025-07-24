import streamlit as st
import numpy as np
from openai import OpenAI
import matplotlib.pyplot as plt
import requests
from io import BytesIO
from PIL import Image
from your_description_db import PRODUCT_DESCRIPTIONS  # from our earlier mapping
from cleaning_products_db import SKUS
import pandas as pd


api_key = st.secrets["OPENAI"]["OPENAI_API_KEY"]
st.session_state["openai"] = OpenAI(api_key=api_key)

def showOpportunities():
    if "location" not in st.session_state:
        location = "Wembley"
        #st.error("Please select location first.")
        #return
    else:
        location = st.session_state["location"]

    # --- Flatten SKUS into a DataFrame ---
    products_data = []
    for category, items in SKUS.items():
        for sku, p in items.items():
            if isinstance(p, dict) and "price_gbp" in p:
                products_data.append({
                    "SKU": sku,
                    "Name": p["name"],
                    "Brand": p["brand"],
                    "Packaging": p["packaging"],
                    "Current Price (£)": p["price_gbp"],
                    "Competitor Price (£)": p["competitor_price_gbp"],
                    "Units Sold Last Week": p["units_sold_last_week"]
                })

    df = pd.DataFrame(products_data)

    # --- Generate Random Suggested Adjustments ---
    np.random.seed()  # optional: comment out for full randomness
    df["Suggested Price Change (£)"] = np.round(np.random.normal(loc=0.0, scale=0.25, size=len(df)), 2)

    # --- Potential Profit Uplift Calculation (£) ---
    # Assume random % uplift, then convert to £
    uplift = np.random.pareto(0.2, size=len(df))
    df["Potential Profit Uplift (£)"] = uplift

    # Drop columns not needed in final display
    df = df.drop(columns=["Units Sold Last Week"])

    # --- Coloring Functions ---
    def color_price_change(val):
        return "color: green;" if val > 0 else "color: red;"

    def color_profit_uplift(val):
        return "color: green;" if val > 100 else ("color: orange;" if val > 30 else "color: red;")

    def color_competitor(val, row):
        diff = val - row["Current Price (£)"]
        if abs(diff) < 0.05:
            return "color: black;"
        elif diff > 0:
            return "color: green;"  # competitor is more expensive → good for us
        else:
            return "color: red;"    # competitor cheaper → bad for us

    # --- Apply Styling ---
    def style_table(df):
        numeric_cols = df.select_dtypes(include=[np.number]).columns

        styled = df.style.apply(
            lambda row: [
                color_competitor(row["Competitor Price (£)"], row)
                if col == "Competitor Price (£)" else ""
                for col in df.columns
            ], axis=1
        )
        styled = styled.applymap(color_price_change, subset=["Suggested Price Change (£)"])
        styled = styled.applymap(color_profit_uplift, subset=["Potential Profit Uplift (£)"])
        styled = styled.format({col: "{:.2f}" for col in numeric_cols})

        # ✅ Properly hide the index (no KeyError)
        styled = styled.hide(axis="index")
        return styled

    # --- Show Table in Streamlit ---
    
    st.title(f"{location}: Uplift opportunities in General CLeaning Products")
    df = df.sort_values(by="Potential Profit Uplift (£)", ascending=False).reset_index(drop=True)
    st.dataframe(style_table(df), use_container_width=True)


def bell_curve(x, mu=0, sigma=1, amplitude=1):
    """Return a bell curve (Gaussian) value for x."""
    return amplitude * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))

def exponential_sample(mean=1.0, size=1):
    """
    Draw random samples from an exponential distribution.
    
    Parameters:
        mean (float): Mean (average time between events), must be > 0.
        size (int): Number of samples to generate.
    
    Returns:
        ndarray or float: Random sample(s).
    """
    return np.random.exponential(scale=mean, size=size)

def showSelector():
    if "location" not in st.session_state:

        st.error("Please select location first.")
        return
    else:
        location = st.session_state["location"]
          

    st.title(f"{location}: Hierarchical Viewer")

    # Main categories and subcategories
    categories = ["Category","GM", "FMCG", "Fashion"]
    subcategories = {
        "GM": ["Electronics", "Home Appliances", "Tools"],
        "FMCG": ["Beverages", "Snacks", "Personal Care", "Cleaning"],
        "Fashion": ["Men's Clothing", "Women's Clothing", "Accessories", "Footwear"],
        "Category":["Subcategory"]
    }
    products = {
        "Electronics": ["Smartphone", "Laptop", "Headphones"],
        "Home Appliances": ["Blender", "Vacuum Cleaner"],
        "Tools": ["Drill", "Hammer"],
        "Beverages": ["Cola", "Orange Juice"],
        "Snacks": ["Chips", "Chocolate Bar"],
        "Personal Care": ["Shampoo", "Toothpaste"],
        "Cleaning": ["Dish Soap", "Laundry Detergent", "General cleaning"],
        "Men's Clothing": ["T-Shirt", "Jeans"],
        "Women's Clothing": ["Dress", "Blouse"],
        "Accessories": ["Handbag", "Watch"],
        "Footwear": ["Sneakers", "Sandals"],
        "Subcategory": ["Product"]
    }

    


    # --- Streamlit UI ---
    CATEGORY = st.selectbox("Select Category", categories)

    if CATEGORY:
        SUB = st.selectbox("Select Subcategory", subcategories[CATEGORY])
        if SUB:
            PROD = st.selectbox("Select Product", products[SUB])
            if PROD:
                if PROD == "General cleaning":
                    SKU = st.selectbox("Select SKU", list(SKUS[PROD].keys()))
                    if SKU and SKU!="SKU":
                        st.write(f"**Selected:** {CATEGORY} → {SUB} → {PROD} → {SKU}")

                        display_product_details(SKUS[PROD][SKU],location)


def display_product_details(p,location):
  

    # --- Basic Info ---
    st.subheader(p["name"])
    st.write(f"**Brand:** {p['brand']}")
    st.write(f"**Description:** {p['description']}")
    st.write(f"**Current Price:** £{p['price_gbp']} ({p['packaging']})")
    st.write(f"**Competitor Price:** £{p['competitor_price_gbp']}")
    st.write(f"**Units Sold Last Week:** {p['units_sold_last_week']}")
    st.write(f"**Margin per Unit:** £{p['margin_per_unit_gbp']}")

    # --- Variables ---
    P0 = p["price_gbp"]
    Q0 = p["units_sold_last_week"]
    PED = p["price_elasticity_slope"]
    unit_cost = P0 - p["margin_per_unit_gbp"]
    competitor_price = p["competitor_price_gbp"]

    # --- Price Range (±25%) ---
    price_range = np.linspace(P0 * 0.75, P0 * 1.25, 40)

    # --- Demand ---
    demand = Q0 * (price_range / P0) ** PED
    demand = np.clip(demand, 0, None)



    # --- Profit Calculation ---
    # NOTE THIS IS ECONOMICALLY INCORRECT, ONLY DESIGNED TO LOOK NICE
    profit = bell_curve(x = price_range, mu = np.random.normal(P0,P0/20), sigma = np.random.normal(P0/5,P0/10), amplitude = exponential_sample(1000,1))

    # Optimal price
    idx = np.argmax(profit)
    optimal_price, optimal_profit = price_range[idx], profit[idx]
    optimal_price  = np.floor(optimal_price * 100)/100

    # --- Plot ---
    fig, ax1 = plt.subplots(figsize=(6, 4))

    ax1.set_xlabel("Price (£)")
    ax1.set_ylabel("Units Sold", color="tab:blue")
    ax1.plot(price_range, demand, color="tab:blue", label="Demand (Units)")
    ax1.tick_params(axis="y", labelcolor="tab:blue")

    ax2 = ax1.twinx()
    ax2.set_ylabel("Total Profit (£/wk/location)", color="tab:green")
    ax2.plot(price_range, profit, color="tab:green", linestyle="--")
    ax2.set_ylim(profit[0], optimal_profit*2 - profit[0])
    ax2.tick_params(axis="y", labelcolor="tab:green")

    # Markers for price levels
    ax2.scatter(optimal_price, optimal_profit, color="red", label=f"Max Profit (£{optimal_price:.2f})")
    idx = np.argmin(np.abs(price_range - P0))
    current_profit = profit[idx]
    ax2.scatter(P0, current_profit, color="orange", label=f"Current (£{P0:.2f})")
    idx = np.argmin(np.abs(price_range - competitor_price))
    comp_profit = profit[idx]
    ax2.scatter(competitor_price, comp_profit, color="purple", label=f"Competitor (£{competitor_price:.2f})")

    # Add legend
    ax2.legend(loc="best")

    plt.title(f"Pricing impact {p['name']}")
    fig.tight_layout()
    st.pyplot(fig)

    if optimal_price > P0:
        #underpriced
        if competitor_price > P0:
            #underpriced and copmaratively cheaper
            st.success("Increase price.")
        else:
            #underpriced but copmaratively expensive
            st.warning("Potential for price increase. Excercise caution.")
    else:
        if competitor_price > P0:
        #overpriced but comparatively cheap
            st.warning("Decrease price. Exercise caution")
        else:
            #overpriced and comparatively expensive
            st.warning("Decrease price.")

    st.write(ask(f"The product in question is {p}. It is sold in a shop in {location}. The optimum price for the product is {optimal_price} leading to {optimal_profit} of profit per week in this location. The profit at the current price is {current_profit}. First provide a single sentence advice regarding pricing of the product. Second provide one paragraph (made-up) explanation for your advice. Quote demographics of the location {location}. (Made-up) past performance of the product. Quote pricing at a competitor. Consider if the product might be a KVI and if that might affect pricing."))
    

def ask(txt):
    message = st.session_state["openai"].chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": txt},
        ],
    )
    return message.choices[0].message.content

showOpportunities()
tab1, tab2, tab3 = st.tabs(["Locations", "Existing Product", "New Product"])

with tab1:
    import folium
    from streamlit_folium import st_folium

    st.title("Select location")

    # Create a folium map centered at a location
    m = folium.Map(location=[51.5074, -0.1278], zoom_start=10)  # London

    # List of pins (latitude, longitude, and popup text)
    stations = [
    (51.50278, -0.12417, "Scotland Yard"),
    (51.4634, -0.0099, "Lewisham"),
    (51.4957, -0.1154, "Brixton"),
    (51.4947, -0.2244, "Hammersmith"),
    (51.5175, -0.116, "Paddington Green"),
    (51.5079, -0.1276, "Charing Cross"),
    (51.5290, -0.1080, "Islington"),
    (51.5260, -0.0940, "Highbury Corner"),
    (51.5075, -0.0876, "Holborn"),
    (51.4080, -0.1510, "Croydon"),
    (51.4120, -0.0560, "Edmonton"),
    (51.4070, -0.1450, "Stoke Newington"),
    (51.4270, -0.1060, "Sutton"),
    (51.4420, -0.3120, "Twickenham"),
    (51.4980, -0.0450, "Stratford"),
    (51.4690, -0.0900, "Wembley"),
    (51.4830, -0.0800, "Walworth"),
    (51.3020, 0.0770, "Dagenham"),
    (51.4070, -0.1290, "Bromley"),
    (51.4480, -0.1640, "Acton"),
]

    # Add pins to the map
    for lat, lon, name in stations:
        folium.Marker(
            location=[lat, lon],
            popup=f"<b>{name}</b>",
            tooltip=name
        ).add_to(m)

    # Display map in Streamlit
    map_data = st_folium(m, width=700, height=500)

    # ✅ Match clicked coords to station name
    if map_data and map_data.get("last_object_clicked"):
        clicked = map_data["last_object_clicked"]
        lat, lon = round(clicked["lat"], 5), round(clicked["lng"], 5)

        for s_lat, s_lon, s_name in stations:
            if round(s_lat, 5) == lat and round(s_lon, 5) == lon:
                st.session_state["location"]=s_name
                break


with tab2:

    showSelector()
                


with tab3:
    
    if "location" not in st.session_state:

        st.error("Please select location first.")
    else:
        location = st.session_state["location"]
        st.title(location)    

     