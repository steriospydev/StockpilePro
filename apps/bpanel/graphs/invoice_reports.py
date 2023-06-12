from django.db.models.functions import TruncMonth
from django.db.models.query import QuerySet
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64

import pandas as pd
import calendar


def construct_overall(invoice_data: QuerySet):
    # Convert invoice data to pandas DataFrame

    df = pd.DataFrame.from_records(invoice_data)
    if df.empty:
        return "No Data Yet!"

    # Extract the year from the month column
    df['year'] = df['month'].dt.year

    # Create a pivot table to show the total for each month and year

    pt = pd.pivot_table(df, index=df['month'].dt.strftime('%m'),
                        columns=df['month'].dt.strftime('%Y'), values='total')

    # Reset the index to make month a column
    pt = pt.reset_index()

    # Create a line plot for each year
    fig, ax = plt.subplots()
    for col in pt.columns[1:]:
        year_data = pt[['month', col]].dropna()
        ax.plot(year_data['month'], year_data[col], label=col)

    ax.set_xticks(pt['month'].unique())

    # Set the chart title and labels
    ax.set_title('Total by Month and Year')
    ax.set_xlabel('Month')
    ax.set_ylabel('Total')
    ax.legend()
    # Save the chart to a PNG image in memory
    buffer = BytesIO()
    ax.get_figure().savefig(buffer, format='png')
    buffer.seek(0)

    # Convert the PNG image to base64 and embed it in HTML
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return image_base64

def construct_month_total_chart(data, year):
    # Filter the data for the specified year
    year_data = [d for d in data if d['month'].year == year]

    # Sort the filtered data by month
    year_data_sorted = sorted(year_data, key=lambda d: d['month'])

    # Extract x and y values from the filtered and sorted data
    x_values = [d['month'].strftime('%B') for d in year_data_sorted]
    y_values = [d['total'] for d in year_data_sorted]

    # Create a bar chart using Matplotlib
    fig, ax = plt.subplots()
    sns.barplot(x=x_values, y=y_values, ax=ax)
    # ax.scatter(x_values, y_values)
    ax.set_title('Total Invoice Amount by Month - {}'.format(year))
    ax.set_xlabel('Month')
    ax.set_ylabel('Total in euro')

    ax.set_xticklabels(x_values, rotation=145)
    ax.grid(True)
    # Add legends for number of invoices and total for the year
    num_invoices = len(year_data)
    total_for_year = sum(y_values)
    ax.text(0.02, 0.95, f'Number of invoices: {num_invoices}', transform=ax.transAxes)
    ax.text(0.02, 0.9, f'Total for the year: €{total_for_year:.2f}', transform=ax.transAxes)
    ax.set_ylim([0, max(y_values)+500])
    # Save the chart to a PNG image in memory
    buffer = BytesIO()
    fig.set_size_inches(12, 10)
    fig.savefig(buffer, format='png')
    buffer.seek(0)

    # Convert the PNG image to base64 and embed it in HTML
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return image_base64
