from bs4 import BeautifulSoup
import json

def extract_articles_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    articles = []
    
    for article in soup.find_all('div', class_='resume-item'):
        # Extract title and link
        title_tag = article.find('h3')
        title = title_tag.text.strip() if title_tag else ""
        link = title_tag.find('a')['href'] if title_tag and title_tag.find('a') else ""
        
        # Extract authors
        authors_tag = article.find('div', class_='subheading')
        authors = authors_tag.decode_contents().strip() if authors_tag else ""
        
        # Extract image source
        img_tag = article.find('img')
        image = img_tag['src'] if img_tag else ""
        
        # Extract description
        desc_tag = article.find('p', style=lambda x: x and 'text-align: justify' in x)
        description = desc_tag.text.strip() if desc_tag else ""
        
        # Append to articles list
        articles.append({
            "title": title,
            "link": link,
            "authors": authors,
            "image": image,
            "description": description
        })
    
    return json.dumps(articles, indent=2)

# Example usage
def save_json_from_html(html, output_file):
    json_data = extract_articles_from_html(html)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(json_data)

html_content = """ 
<!-- Article -2 Starts -->
<div class="resume-item d-flex flex-column flex-md-row justify-content-between mb-5">
  <div class="resume-content">
    <h3 class="mb-0"><a href="https://www.cs.ucdavis.edu/~filkov/papers/react.pdf" target="_blank">From Models to Practice: Enhancing OSS Project Sustainability with Evidence-Based Advice</a></h3>
    <div class="subheading mb-3"><b>Nafiz Imtiaz Khan</b>, Vladimir Filkov</div>


    <p style="text-align: justify;">

      Sustainability in Open Source Software (OSS) projects is crucial for long-term innovation, community support, and the enduring success of open-source solutions. Although multitude of studies have provided effective models for OSS sustainability, their practical implications have been lacking because most identified features are not amenable to direct tuning by developers (e.g., levels of communication, number of commits per project). 

      In this paper, we report on preliminary work toward making models more actionable based on evidence-based findings from prior research. Given a set of identified features of interest to OSS project sustainability, we performed a comprehensive literature review related to those features to uncover practical, evidence-based advice, which we call Researched Actionables (ReACTs). The ReACTs are practical advice with specific steps, found in prior work to associate with tangible results. Starting from a set of sustainability-related features, this study contributes 105 ReACTs to the SE community by analyzing 186 published articles. Moreover, this study introduces a newly developed tool (ReACTive) designed to enhance the exploration of ReACTs through visualization across various facets of the OSS ecosystem. The ReACTs idea opens new avenues for connecting SE metrics to actionable research in SE in general.

   </p>
    </div>
 
    <div class="col-lg-4 col-md-4 col-sm-12">
      <img class="img-fluid" src="img/react_paper.png" alt="">
    </div>
</div>
<!-- Article Ends -->


<!-- Article -1 Starts -->
<div class="resume-item d-flex flex-column flex-md-row justify-content-between mb-5">
  <div class="col-lg-4 col-md-4 col-sm-12">
    <img class="img-fluid" src="img/EvidenceBotArchitecture.png" alt="">
  </div>

  <div class="resume-content">
    <h3 class="mb-0"><a href="" target="_blank">Leveraging Language Models to Discover Evidence-Based Actions for OSS Sustainability</a></h3>
    <div class="subheading mb-3"><b>Nafiz Imtiaz Khan</b>, Vladimir Filkov</div>


    <p style="text-align: justify;">

      When successful, Open Source Software (OSS) projects can provide tremendous economic value for society, but the road to their success is not straightforward. Keeping a project on the trajectory to success calls for effective and actionable models for forecasting their sustainability. However, the distributed, multilayered structures of OSS projects make it challenging for practitioners to map model features to specific actions. Consequently, there is a pressing need for actionable recommendations derived from empirical evidence, coming out of prior studies which have established direct links between model features and actionable outcomes.

      In this study, we propose a Retrieval-Augmented Generation (RAG)-based pipeline that employs a combination of traditional and strategic LLM prompting techniques to extract actionable recommendations from scientific articles in Software Engineering. Our two-layered approach first utilizes conventional prompting to identify actionables, followed by a follow-up prompting technique to supplement these insights with contextual information, enhancing their practical applicability. Through a comprehensive analysis of 823 articles published in top-ranked Software Engineering venues in the 21st century, we have extracted 2,234 actionable recommendations. This research not only addresses potential concerns of using Large Language Models (LLMs) for such tasks but also provides a robust methodology for deriving and evaluating actionable insights. The adaptation of these recommendations has the potential to aid thousands of OSS projects that may be at risk at any given time, potentially saving valuable resources.

   </p>
    </div>
 
    
</div>


"""
save_json_from_html(html_content, 'output.json')
