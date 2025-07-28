import streamlit as st
import pandas as pd
from datetime import datetime

# ====== CSS STYLING ======
st.markdown("""
<style>
    /* Main container styling */
    .main-container {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Header styling */
    .header {
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1.5rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
    }
    
    /* Color display box */
    .color-display {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Color swatch */
    .color-swatch {
        display: inline-block;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        margin-right: 10px;
        vertical-align: middle;
        border: 2px solid #dee2e6;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: #3498db;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        border: none;
    }
    
    /* Footer */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        text-align: center;
        padding: 1rem;
        background-color: black;
        border-top: 1px solid #dee2e6;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ====== APP INITIALIZATION ======
if 'orders' not in st.session_state:
    st.session_state.orders = pd.DataFrame(columns=[
        'Order Date', 'Customer Name', 'Sport', 'Jersey Type', 
        'Size', 'Color', 'Quantity', 'Image', 'Payment Status', 'Total Amount'
    ])
if 'exported' not in st.session_state:
    st.session_state.exported = False  # Track if the data has been exported

# ====== FUNCTION DEFINITIONS ======
def get_most_popular_color():
    if st.session_state.orders.empty:
        return None, 0
    color_counts = st.session_state.orders['Color'].value_counts()
    return color_counts.idxmax(), color_counts.max()

def rgb_to_hex(rgb_str):
    """Convert RGB string to hex color"""
    rgb = rgb_str.strip('rgb(').strip(')').split(',')
    return "#{:02x}{:02x}{:02x}".format(*map(int, rgb))

# ====== MAIN APP LAYOUT ======
st.sidebar.title("Navigation")
tab = st.sidebar.radio("Select a tab", ["Place New Order", "View Analytics"])

if tab == "Place New Order":
    st.markdown('<h1 class="header">⚽ Jersey Order Management</h1>', unsafe_allow_html=True)
    
    with st.form("order_form", clear_on_submit=True):
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        
        st.subheader("Customer Information")
        customer_name = st.text_input("Full Name*", placeholder="Enter your name")
        customer_email = st.text_input("Email*", placeholder="example@gmail.com")  # Email input
        
        st.subheader("Jersey Details")
        col1, col2 = st.columns(2)
        with col1:
            sport = st.selectbox("Sport*", ["Football", "Basketball", "Cricket", "Volleyball", "Other"])
            jersey_type = st.selectbox("Jersey Type*", ["Home", "Away", "Special Edition"])
            size = st.select_slider("Size*", options=['XS', 'S', 'M', 'L', 'XL', 'XXL'])
        with col2:
            color = st.selectbox("Jersey Color*", ["#3498db", "#808080", "#ff5733", "#28a745", "#ffc107"], format_func=lambda x: f"Color: {x}" if x != "#808080" else "Color: Grey")
            quantity = st.number_input("Quantity*", 1, 100, 1)
        
        # Image upload
        jersey_image = st.file_uploader("Upload Jersey Image", type=["jpg", "jpeg", "png"])
        
        # Submit button for order
        submitted = st.form_submit_button("Submit Order", type="primary")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if submitted:
            if not customer_name or not customer_email:
                st.error("Please enter both your name and email address.")
            else:
                # Convert the uploaded image to bytes
                image_bytes = jersey_image.read() if jersey_image is not None else None
                
                # Calculate total amount
                total_amount = quantity * 20  # Example price per jersey
                
                new_order = {
                    'Order Date': datetime.now(),
                    'Customer Name': customer_name,
                    'Sport': sport,
                    'Jersey Type': jersey_type,
                    'Size': size,
                    'Color': color,
                    'Quantity': quantity,
                    'Image': image_bytes,  # Store image as bytes
                    'Payment Status': 'done',  # Default payment status
                    'Total Amount': total_amount  # Store total amount
                }
                new_order_df = pd.DataFrame([new_order])
                
                # Check if the new order DataFrame is not empty
                if not new_order_df.empty:
                    st.session_state.orders = pd.concat([
                        st.session_state.orders,
                        new_order_df
                    ], ignore_index=True)
                
                # Display the uploaded image
                if jersey_image is not None:
                    st.image(jersey_image, caption='Uploaded Jersey Image', use_container_width=True)

                # Payment section
                st.subheader("Payment")
                st.markdown(f"Total Amount: ${total_amount}")

                # Create a mock payment button inside the form
                if st.form_submit_button("Confirm Payment"):
                    st.success("Payment successful! Order submitted.")
                    # Update payment status
                    st.session_state.orders.at[st.session_state.orders.index[-1], 'Payment Status'] = 'Paid'
                    st.image(jersey_image, caption='Uploaded Jersey Image', use_container_width=True)  # Show image after payment

elif tab == "View Analytics":
    st.markdown('<h1 class="header">⚽ Order Analytics</h1>', unsafe_allow_html=True)
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Total Orders Count
    total_orders = len(st.session_state.orders)
    st.subheader("Total Orders")
    st.markdown(f"**Total Orders:** {total_orders}")

    # Popular Color Display
    popular_color, count = get_most_popular_color()
    if popular_color:
        hex_color = popular_color if popular_color.startswith('#') else rgb_to_hex(popular_color)
        
        st.subheader("Most Popular Color")
        st.markdown(f"""
        <div class="color-display">
            <span class="color-swatch" style="background-color:{hex_color};"></span>
            <strong>Color:</strong> {hex_color.upper()}<br>
            <strong>Orders:</strong> {count}
        </div>
        """, unsafe_allow_html=True)
        
        # Visualizations
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Color Distribution")
            st.bar_chart(st.session_state.orders['Color'].value_counts())
        with col2:
            st.subheader("Size Distribution")
            st.bar_chart(st.session_state.orders['Size'].value_counts())
    else:
        st.info("No orders yet. Create your first order in the 'Place New Order' tab.")
        
    st.markdown('</div>', unsafe_allow_html=True)

# ====== FOOTER ======
st.markdown("""
<div class="footer">
    Jersey Order Management System © 2025
</div>
""", unsafe_allow_html=True)

# ====== DATA EXPORT ======
with st.expander("View/Export All Orders"):
    st.write(st.session_state.orders)
    if not st.session_state.orders.empty:
        if not st.session_state.exported:
            if st.download_button(
                "Export to CSV",
                st.session_state.orders.to_csv(index=False),
                "jersey_orders.csv",
                "text/csv"
            ):
                st.session_state.exported = True  # Mark as exported
                st.success("Data exported successfully!")
        else:
            st.info("Data has already been exported. You can save the next data.")
