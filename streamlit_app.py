import streamlit as st
import numpy as np
from openai import OpenAI
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
from your_description_db import PRODUCT_DESCRIPTIONS  # from our earlier mapping
from cleaning_products_db import SKUS
import pandas as pd

st.set_page_config(layout="wide")

api_key = st.secrets["OPENAI"]["OPENAI_API_KEY"]
st.session_state["openai"] = OpenAI(api_key=api_key)

def showOpportunities():
    if "location" not in st.session_state:
        st.error("Please select location first.")
        return
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
    df["Suggested Price Change (£)"] = np.round(np.maximum(np.minimum(np.random.standard_t(2, size=len(df)),df["Current Price (£)"]*.3),df["Current Price (£)"]*-0.3), 2)

    # --- Potential Profit Uplift Calculation (£) ---
    # Assume random % uplift, then convert to £
    uplift = 100*np.abs(np.random.pareto(1, size=len(df))* df["Suggested Price Change (£)"])
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
    

    def recommendation(row):
        # 1) Optimal price if uplift < 20
        if row["Potential Profit Uplift (£)"] < 20:
            return "✅ Optimal price"  # (green letters in Streamlit can be added with markdown)
        
        # 2) Redistribution condition
        if (
            row["Current Price (£)"] > row["Competitor Price (£)"] and
            (row["Current Price (£)"] + row["Suggested Price Change (£)"]) > row["Competitor Price (£)"]
        ):
            return "Redistribution"
        
        # 3 & 4) Increase or Decrease depending on directionality
        if row["Suggested Price Change (£)"] > 0:
            return "Increase price"
        elif row["Suggested Price Change (£)"] < 0:
            return "Decrease price"
        else:
            return "No change"
        
    df["Recommendation"] = df.apply(recommendation, axis=1)

    def recommendation_with_arrows(row):

        # 3 & 4) Increase or Decrease depending on directionality
        if row["Recommendation"] == "Increase price":
            return "🟢 Increase price"
        elif row["Recommendation"] == "Decrease price":
            return "🔴 Decrease price"
        elif row["Recommendation"] == "Redistribution":
            return "🔄 Redistribution"
        elif row["Recommendation"] == "✅ Optimal price":
            return "✅ Optimal price"
        


    df["Recommendation"] = df.apply(recommendation_with_arrows, axis=1)

    st.title(f"{location}: Uplift opportunities in General Cleaning Products")
    df = df.sort_values(by="Potential Profit Uplift (£)", ascending=False).reset_index(drop=True)
    df.set_index("SKU", inplace=True)
    st.dataframe(style_table(df))


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
          

    st.title(f"{location}: SKU Viewer")

    # Main categories and subcategories
    #categories = ["Category","GM", "FMCG", "Fashion"]
    categories = ["FMCG"]
    subcategories = {
        #"GM": ["Electronics", "Home Appliances", "Tools"],
        #"FMCG": ["Beverages", "Snacks", "Personal Care", "Cleaning"],
        "FMCG": ["Cleaning"],
        #"Fashion": ["Men's Clothing", "Women's Clothing", "Accessories", "Footwear"],
        #"Category":["Subcategory"]
    }
    products = {
        #"Electronics": ["Smartphone", "Laptop", "Headphones"],
        #"Home Appliances": ["Blender", "Vacuum Cleaner"],
        #"Tools": ["Drill", "Hammer"],
        #"Beverages": ["Cola", "Orange Juice"],
        #"Snacks": ["Chips", "Chocolate Bar"],
        #"Personal Care": ["Shampoo", "Toothpaste"],
        #"Cleaning": ["Dish Soap", "Laundry Detergent", "General cleaning"],
        "Cleaning": ["Detergents"],
        #"Men's Clothing": ["T-Shirt", "Jeans"],
        #"Women's Clothing": ["Dress", "Blouse"],
        #"Accessories": ["Handbag", "Watch"],
        #"Footwear": ["Sneakers", "Sandals"],
        #"Subcategory": ["Product"]
    }

    


    # --- Streamlit UI ---
    CATEGORY = st.selectbox("Select Category", categories)

    if CATEGORY:
        SUB = st.selectbox("Select Subcategory", subcategories[CATEGORY])
        if SUB:
            PROD = st.selectbox("Select Product", products[SUB])
            if PROD:
                if PROD == "Detergents":
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
    profit = bell_curve(x = price_range, mu = np.random.normal(P0,P0/10), sigma = np.random.normal(P0/4,P0/10), amplitude = exponential_sample(1000,1))

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
    ax2.set_ylim(0, optimal_profit*2 - profit[0])
    ax2.tick_params(axis="y", labelcolor="tab:green")

    # Markers for price levels
    ax2.scatter(optimal_price, optimal_profit, color="red", label=f"Most profitable: £{optimal_price:.2f}/unit")
    idx = np.argmin(np.abs(price_range - P0))
    current_profit = profit[idx]
    ax2.scatter(P0, current_profit, color="orange", label=f"Current: £{P0:.2f}/unit")
    idx = np.argmin(np.abs(price_range - competitor_price))
    comp_profit = profit[idx]
    ax2.scatter(competitor_price, comp_profit, color="purple", label=f"Competitor: £{competitor_price:.2f}/unit")

    # Add legend
    ax2.legend(loc="best")

    plt.title(f"Pricing impact {p['name']}")
    fig.tight_layout()
    st.pyplot(fig)

    if np.abs(optimal_profit-current_profit) < 20:
        st.warning("The product seems to be priced close to opimal amount.")
    else:
        if optimal_price > P0:
            #underpriced
            if competitor_price > P0:
                #underpriced and copmaratively cheaper
                st.error("Increase price.")
            else:
                #underpriced but copmaratively expensive
                st.warning("Potential for price increase. Excercise caution.")
        else:
            if competitor_price > P0:
            #overpriced but comparatively cheap
                st.warning("Consider moving the stock to a different store.")
            else:
                #overpriced and comparatively expensive
                st.warning("Decrease price.")

        st.write(ask(f"The product in question is {p}. It is sold in a shop in {location}. The optimum price for the product is {optimal_price} leading to {optimal_profit} of profit per week in this location. The profit at the current price is {current_profit}. First provide a single sentence advice regarding pricing of the product. Only in cases where the product is priced lower than competitor and the the optimum price is even higher than the competitor you should suggest to move the stock to a different store instead of changing the price. Second provide 4-6 bullet-point (made-up) explanation for your advice. Quote demographics of the location {location}. (Made-up) past performance of the product. Quote pricing at a competitor. Consider if the product might be a KVI and if that might affect pricing. If the advice is to move the stock to a different store, name the store to move the stock to including a brief explanation why that store is more suitable. (if it indeed is recommendable to move the stock suggest one of the following stores: Scotland Yard, Lewisham, Brixton, Hammersmith, Paddington Green, Charing Cross, Islington, Highbury Corner, Holborn, Croydon, Edmonton, Stoke Newington, Sutton, Twickenham, Stratford, Wembley, Walworth, Dagenham, Bromley, Acton)."))
        
def storeSelector():
    st.title("Select store")

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


def ask(txt):
    message = st.session_state["openai"].chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": txt},
        ],
    )
    return message.choices[0].message.content

tab1, tab2, tab3 = st.tabs(["Locations", "Products", "Uplift Opportunities"])

with tab1:

    storeSelector()
    

with tab2:

    showSelector()
                


with tab3:  

    showOpportunities()

     