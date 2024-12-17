import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
import os

# Set Seaborn style
sns.set(style="whitegrid")

# 1. Load Data
data_file = 'users_combined_info_500.csv'
if not os.path.exists(data_file):
    raise FileNotFoundError(f"The data file {data_file} does not exist in the current directory.")

# Read CSV data
df = pd.read_csv(data_file)

# Display first few rows to verify
print("First few rows of the dataset:")
print(df.head())

# 2. Data Preprocessing
# Convert 'event_time' to datetime object
df['event_time'] = pd.to_datetime(df['event_time'])

# Extract city information (assuming 'location' format is "City, State")
df['city'] = df['location'].apply(lambda x: x.split(',')[0].strip())

# Extract UTC offset
df['utc_offset'] = df['event_time'].dt.strftime('%z')

# 3. Demographic Analysis

## 3.1 Country and Region Distribution
country_distribution = df['country'].value_counts()
print("\nCountry Distribution:")
print(country_distribution)

## 3.2 City-level Distribution
city_distribution = df['city'].value_counts()
print("\nCity Distribution:")
print(city_distribution)

## 3.3 Timezone Distribution
timezone_distribution = df['utc_offset'].value_counts()
print("\nTimezone (UTC Offset) Distribution:")
print(timezone_distribution)

# 4. Collaboration Behavior Analysis

## 4.1 Submission Frequency
submission_frequency = df.groupby('user_id').size().reset_index(name='submission_count')
high_active_threshold = submission_frequency['submission_count'].quantile(0.75)
low_active_threshold = submission_frequency['submission_count'].quantile(0.25)
high_active_users = submission_frequency[submission_frequency['submission_count'] > high_active_threshold]
low_active_users = submission_frequency[submission_frequency['submission_count'] < low_active_threshold]
print("\nSubmission Frequency:")
print(submission_frequency)

print("\nHigh Active Users:")
print(high_active_users)

print("\nLow Active Users:")
print(low_active_users)

# 5. Additional Insights

## 5.1 Influence vs Submission Frequency
influence_submission = df.groupby('user_id').agg(
    total_submissions=pd.NamedAgg(column='event_action', aggfunc='count'),
    total_influence=pd.NamedAgg(column='total_influence', aggfunc='first')  # Assuming influence is same per user
).reset_index()
print("\nInfluence vs Submission Frequency:")
print(influence_submission.head())

## 5.2 Event Action Types Distribution
event_action_distribution = df['event_action'].value_counts()
print("\nEvent Action Distribution:")
print(event_action_distribution)

# 6. Visualization

# Create a directory to save plots
plots_dir = 'plots'
if not os.path.exists(plots_dir):
    os.makedirs(plots_dir)

## 6.1 Country Distribution Plot
plt.figure(figsize=(10,6))
sns.barplot(x=country_distribution.index, y=country_distribution.values, palette='viridis')
plt.title('Country Distribution of Users')
plt.xlabel('Country')
plt.ylabel('Number of Users')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'country_distribution.png'))
plt.close()

## 6.2 City Distribution Plot (Top 10 Cities)
top_cities = city_distribution.head(10)
plt.figure(figsize=(12,8))
sns.barplot(x=top_cities.values, y=top_cities.index, palette='magma')
plt.title('Top 10 Cities by Developer Density')
plt.xlabel('Number of Users')
plt.ylabel('City')
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'city_distribution.png'))
plt.close()

## 6.3 Timezone Distribution Plot
plt.figure(figsize=(10,6))
sns.barplot(x=timezone_distribution.index, y=timezone_distribution.values, palette='coolwarm')
plt.title('Timezone (UTC Offset) Distribution of Users')
plt.xlabel('UTC Offset')
plt.ylabel('Number of Users')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'timezone_distribution.png'))
plt.close()

## 6.4 Submission Frequency Distribution Plot
plt.figure(figsize=(10,6))
sns.histplot(submission_frequency['submission_count'], bins=30, kde=True, color='skyblue')
plt.title('Submission Frequency Distribution')
plt.xlabel('Number of Submissions')
plt.ylabel('Number of Users')
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'submission_frequency.png'))
plt.close()

## 6.5 Influence vs Submission Frequency Scatter Plot
plt.figure(figsize=(10,6))
sns.scatterplot(data=influence_submission, x='total_submissions', y='total_influence', hue='total_submissions', palette='deep')
plt.title('Influence vs Submission Frequency')
plt.xlabel('Total Submissions')
plt.ylabel('Total Influence')
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'influence_submission.png'))
plt.close()

## 6.6 Event Action Types Distribution Plot
plt.figure(figsize=(8,6))
sns.countplot(data=df, x='event_action', palette='Set2')
plt.title('Event Action Types Distribution')
plt.xlabel('Event Action')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'event_action_distribution.png'))
plt.close()

# 7. Generate PDF Report

class PDFReport(FPDF):
    def __init__(self):
        super().__init__()
        self.add_page()  # Add a page upon initialization
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        # Set title
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Data Insights Report', border=False, ln=1, align='C')
        self.ln(10)

    def chapter_title(self, title):
        # Set chapter title
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, title, ln=1, align='L')
        self.ln(5)

    def add_image_with_caption(self, image_path, caption):
        # Add image
        if os.path.exists(image_path):
            self.image(image_path, w=180)
            self.ln(5)
            # Add caption
            self.set_font('Arial', '', 12)
            self.multi_cell(0, 10, caption)
            self.ln()
        else:
            print(f"Image {image_path} not found. Skipping.")

# Initialize PDF
pdf = PDFReport()

# 1. Demographic Analysis
pdf.chapter_title('1. Demographic Analysis')

# 1.1 Country and Region Distribution
pdf.chapter_title('1.1 Country and Region Distribution')
pdf.add_image_with_caption(os.path.join(plots_dir, 'country_distribution.png'), 'Figure 1: Country Distribution of Users. This chart shows the concentration of users across different countries.')

# 1.2 City-level Distribution
pdf.chapter_title('1.2 City-level Distribution')
pdf.add_image_with_caption(os.path.join(plots_dir, 'city_distribution.png'), 'Figure 2: Top 10 Cities by Developer Density. This chart illustrates the distribution of developers in major cities, helping to identify technology hotspots.')

# 1.3 Timezone Distribution
pdf.chapter_title('1.3 Timezone Distribution')
pdf.add_image_with_caption(os.path.join(plots_dir, 'timezone_distribution.png'), 'Figure 3: Timezone (UTC Offset) Distribution of Users. This chart helps understand the collaboration time patterns of users from different regions.')

# 2. Collaboration Behavior Analysis
pdf.chapter_title('2. Collaboration Behavior Analysis')

# 2.1 Submission Frequency
pdf.chapter_title('2.1 Submission Frequency')
pdf.add_image_with_caption(os.path.join(plots_dir, 'submission_frequency.png'), 'Figure 4: Submission Frequency Distribution. This chart identifies high-active and low-active users based on their submission counts.')

# 2.2 High Active Users
pdf.chapter_title('2.2 High Active Users')
pdf.set_font('Arial', '', 12)
pdf.multi_cell(0, 10, f"High active users are those in the top 25% of submission counts, totaling {len(high_active_users)} users.")
pdf.ln()

# 2.3 Low Active Users
pdf.chapter_title('2.3 Low Active Users')
pdf.multi_cell(0, 10, f"Low active users are those in the bottom 25% of submission counts, totaling {len(low_active_users)} users.")
pdf.ln()

# 3. Additional Insights
pdf.chapter_title('3. Additional Insights')

# 3.1 Influence vs Submission Frequency
pdf.chapter_title('3.1 Influence vs Submission Frequency')
pdf.add_image_with_caption(os.path.join(plots_dir, 'influence_submission.png'), 'Figure 5: Influence vs Submission Frequency. This scatter plot analyzes the relationship between user influence and their submission counts.')

# 3.2 Event Action Types Distribution
pdf.chapter_title('3.2 Event Action Types Distribution')
pdf.add_image_with_caption(os.path.join(plots_dir, 'event_action_distribution.png'), 'Figure 6: Event Action Types Distribution. This chart displays the distribution of different event actions.')

# Save PDF
report_file = 'Data_Insights_Report.pdf'
pdf.output(report_file)
print(f"\nPDF report generated successfully: {report_file}")
