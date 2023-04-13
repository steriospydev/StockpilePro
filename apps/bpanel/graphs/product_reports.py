import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pandas as pd
def construct_product_chart(product):
    # Create a list of labels and values from the product queryset
    name = [p['product_name'] for p in product]
    labels = [p['package_str'] for p in product]
    total_bought = [p['total_bought'] for p in product]
    total_sold = [p['total_sold'] for p in product]
    total_available = [p['total_available'] for p in product]

    # Set the color palette
    sns.set_palette("dark")

    # Create the bar chart using seaborn
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=['Αγορες', 'Πωλήσεις'], y=[sum(total_bought), sum(total_sold)], ax=ax)

    # Set the labels and title
    ax.set_xlabel('')
    ax.set_ylabel('Quantity')
    ax.set_title(f"{name[0]}-{labels[0]}")
    chart_title = f"Διαθέσιμα: {sum(total_available) or None}"
    ax.legend(title=chart_title, loc='upper left')
    # Reverse the orientation of the axes
    ax.invert_xaxis()

    # Save the chart to a PNG image in memory
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Convert the PNG image to base64 and embed it in HTML
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return image_base64
