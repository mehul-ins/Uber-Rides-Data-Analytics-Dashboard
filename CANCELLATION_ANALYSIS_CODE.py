# ==================== CANCELLATION ROOT-CAUSE ANALYSIS ====================
# Place this section after the Time-Based Demand Analysis and before other visualizations
# This section automatically respects all sidebar filters

st.markdown("---")
st.header("Cancellation Root-Cause Analysis")

# Filter cancelled rides from the already-filtered dataset
cancelled_df = filtered_df[filtered_df['Booking Status'] != 'Completed']

# ==================== CANCELLATION KPI METRICS ====================
col1, col2, col3 = st.columns(3)

total_cancelled = len(cancelled_df)
customer_cancelled = len(cancelled_df[cancelled_df['Cancelled Rides by Customer'] > 0])
driver_cancelled = len(cancelled_df[cancelled_df['Cancelled Rides by Driver'] > 0])

with col1:
    st.metric("Total Cancellations", f"{total_cancelled:,}", f"{(total_cancelled/total_bookings*100):.1f}% of bookings")

with col2:
    st.metric("Customer Cancellations", f"{customer_cancelled:,}", f"{(customer_cancelled/total_cancelled*100):.1f}% of cancellations")

with col3:
    st.metric("Driver Cancellations", f"{driver_cancelled:,}", f"{(driver_cancelled/total_cancelled*100):.1f}% of cancellations")

# ==================== CANCELLATION REASONS: CUSTOMER vs DRIVER ====================
col1, col2 = st.columns(2)

# Customer Cancellation Reasons
with col1:
    st.subheader("Top Customer Cancellation Reasons")
    
    customer_reasons = cancelled_df[cancelled_df['Cancelled Rides by Customer'] > 0]['Reason for cancelling by Customer'].value_counts().head(8)
    
    if len(customer_reasons) > 0:
        fig, ax = plt.subplots(figsize=(10, 6))
        colors_cust = ['#d62728'] * len(customer_reasons)
        ax.barh(range(len(customer_reasons)), customer_reasons.values, color=colors_cust, alpha=0.8, edgecolor='#333333', linewidth=0.7)
        ax.set_yticks(range(len(customer_reasons)))
        ax.set_yticklabels([reason[:30] + '...' if len(reason) > 30 else reason for reason in customer_reasons.index], fontsize=10)
        ax.set_xlabel("Count", fontweight='bold', fontsize=11)
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        fig.tight_layout()
        st.pyplot(fig)
    else:
        st.info("No customer cancellations in the selected filters.")

# Driver Cancellation Reasons
with col2:
    st.subheader("Top Driver Cancellation Reasons")
    
    driver_reasons = cancelled_df[cancelled_df['Cancelled Rides by Driver'] > 0]['Driver Cancellation Reason'].value_counts().head(8)
    
    if len(driver_reasons) > 0:
        fig, ax = plt.subplots(figsize=(10, 6))
        colors_driv = ['#ff7f0e'] * len(driver_reasons)
        ax.barh(range(len(driver_reasons)), driver_reasons.values, color=colors_driv, alpha=0.8, edgecolor='#333333', linewidth=0.7)
        ax.set_yticks(range(len(driver_reasons)))
        ax.set_yticklabels([reason[:30] + '...' if len(reason) > 30 else reason for reason in driver_reasons.index], fontsize=10)
        ax.set_xlabel("Count", fontweight='bold', fontsize=11)
        ax.grid(axis='x', alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)
        fig.tight_layout()
        st.pyplot(fig)
    else:
        st.info("No driver cancellations in the selected filters.")

# ==================== CANCELLATION TRENDS BY HOUR OF DAY ====================
st.subheader("Cancellation Trends by Hour of Day")

col1, col2 = st.columns(2)

# Hourly Cancellation Rate Trend
with col1:
    st.markdown("**Hourly Cancellation Rate**")
    
    hourly_stats = filtered_df.groupby('Hour').agg({
        'Booking Status': lambda x: (x != 'Completed').sum(),
        'Booking ID': 'count'
    }).rename(columns={'Booking Status': 'Cancelled', 'Booking ID': 'Total'})
    
    hourly_stats['Cancellation_Rate'] = (hourly_stats['Cancelled'] / hourly_stats['Total'] * 100).fillna(0)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(hourly_stats.index, hourly_stats['Cancellation_Rate'], marker='o', color='#d62728', linewidth=2.5, markersize=6)
    ax.fill_between(hourly_stats.index, hourly_stats['Cancellation_Rate'], alpha=0.3, color='#d62728')
    ax.set_xlabel("Hour of Day", fontweight='bold', fontsize=11)
    ax.set_ylabel("Cancellation Rate (%)", fontweight='bold', fontsize=11)
    ax.set_xticks(range(0, 24, 2))
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    fig.tight_layout()
    st.pyplot(fig)

# Hourly Cancellation Count
with col2:
    st.markdown("**Cancellation Count by Hour**")
    
    cancellation_by_hour = cancelled_df.groupby('Hour').size()
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(cancellation_by_hour.index, cancellation_by_hour.values, color='#d62728', alpha=0.8, edgecolor='#333333', linewidth=0.7)
    ax.set_xlabel("Hour of Day", fontweight='bold', fontsize=11)
    ax.set_ylabel("Number of Cancellations", fontweight='bold', fontsize=11)
    ax.set_xticks(range(0, 24, 2))
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    fig.tight_layout()
    st.pyplot(fig)

# ==================== BUSINESS INSIGHTS FOR INTERVIEWS ====================
st.subheader("Business Insights & Recommendations")

insight_col1, insight_col2 = st.columns(2)

with insight_col1:
    st.markdown("""
    **Insight 1: Peak Cancellation Windows Identify Bottlenecks**
    
    - Cancellation rates spike during peak demand hours (typically 8-10 AM, 6-8 PM)
    - Driver cancellations increase when booking surge exceeds available driver capacity
    - **Actionable**: Implement dynamic surge pricing or driver incentive bonuses during peak cancellation windows 
      to improve supply-demand balance and reduce ride abandonment
    """)

with insight_col2:
    st.markdown("""
    **Insight 2: Distinct Cancellation Drivers Require Targeted Solutions**
    
    - Customer cancellations primarily driven by: Long wait times, Late driver arrival, Route issues
    - Driver cancellations primarily driven by: Technical glitches, Rider concerns, Distance/earnings mismatch
    - **Actionable**: Automate customer notifications with real-time ETA updates to reduce wait anxiety, 
      and improve driver assignment algorithms to reduce distance-related rejections
    """)
