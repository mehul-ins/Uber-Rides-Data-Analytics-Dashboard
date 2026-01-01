# ==================== KPI SECTION ====================
st.header("KPI Overview")

col1, col2, col3, col4 = st.columns(4)

# Calculate KPIs
total_bookings = len(filtered_df)
total_revenue = filtered_df['Booking Value'].sum()
cancelled_bookings = len(filtered_df[filtered_df['Booking Status'] != 'Completed'])
cancellation_rate = (cancelled_bookings / total_bookings * 100) if total_bookings > 0 else 0
peak_hour = int(filtered_df['Hour'].mode()[0]) if len(filtered_df['Hour'].mode()) > 0 else 0

with col1:
    st.metric("Total Bookings", f"{total_bookings:,}")

with col2:
    st.metric("Total Revenue", f"₹{total_revenue:,.0f}")

with col3:
    st.metric("Cancellation Rate", f"{cancellation_rate:.1f}%")

with col4:
    st.metric("Peak Hour", f"{peak_hour:02d}:00")


# ==================== TIME-BASED DEMAND CHARTS ====================
st.header("Time-Based Demand Analysis")

col1, col2 = st.columns(2)

# Hourly Demand Chart
with col1:
    st.subheader("Hourly Demand Trend")
    
    hourly_data = filtered_df.groupby('Hour').size()
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(hourly_data.index, hourly_data.values, color='#1f77b4', alpha=0.8, edgecolor='#333333', linewidth=0.7)
    ax.set_xlabel("Hour of Day", fontweight='bold', fontsize=11)
    ax.set_ylabel("Number of Bookings", fontweight='bold', fontsize=11)
    ax.set_xticks(range(0, 24, 2))
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    fig.tight_layout()
    st.pyplot(fig)

# Day-wise Trend Chart
with col2:
    st.subheader("Day-wise Booking Trend")
    
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily_data = filtered_df['Day'].value_counts().reindex(day_order, fill_value=0)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ['#2ca02c' if day not in ['Saturday', 'Sunday'] else '#ff7f0e' for day in day_order]
    ax.bar(range(len(daily_data)), daily_data.values, color=colors, alpha=0.8, edgecolor='#333333', linewidth=0.7)
    ax.set_xticks(range(len(day_order)))
    ax.set_xticklabels([day[:3] for day in day_order], fontsize=10)
    ax.set_ylabel("Number of Bookings", fontweight='bold', fontsize=11)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    fig.tight_layout()
    st.pyplot(fig)
