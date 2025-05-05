import wikipedia
from youtube_transcript_api import YouTubeTranscriptApi
import requests
import os
import re
from urllib.parse import urlparse, parse_qs
import json

def get_tool_names():
    return [
        "Wikipedia Tool",
        "Study Tips Tool",
        "Google Search Tool",
        "YouTube Summary Tool",
        "Exam Strategy Tool",
        "Flashcard Generator Tool",
        "Note Organizer Tool",
        "Concept Mapper Tool",
        "Scholarly Papers Tool",
        "Subject Expert Tool"
    ]

def wikipedia_tool(query: str) -> str:
    try:
        wikipedia.set_lang("en")
        search_results = wikipedia.search(query)
        if not search_results:
            return f"No Wikipedia results found for '{query}'."
        
        page_title = search_results[0]
        page = wikipedia.page(page_title, auto_suggest=False)
        summary = wikipedia.summary(page_title, sentences=5)
        
        return f"📚 Wikipedia: {page_title}\n\n{summary}\n\nSource: {page.url}"
    except wikipedia.DisambiguationError as e:
        return f"Multiple Wikipedia entries found. Try one of these: {', '.join(e.options[:5])}"
    except wikipedia.PageError:
        return f"No Wikipedia page found for '{query}'."
    except Exception as e:
        return f"Couldn't fetch Wikipedia content: {str(e)}"

def study_tips_tool(query: str) -> str:
    try:
        api_key = os.getenv("SERPAPI_API_KEY")
        if not api_key:
            return "Missing SerpAPI key. Please set the SERPAPI_API_KEY environment variable."
        
        search_query = f"study tips for {query}"
        params = {
            "q": search_query,
            "api_key": api_key,
            "engine": "google",
            "num": 3
        }
        
        response = requests.get("https://serpapi.com/search", params=params)
        if response.status_code != 200:
            return f"Failed to fetch study tips. Status code: {response.status_code}"
        
        data = response.json()
        results = data.get("organic_results", [])
        
        if not results:
            return f"No study tips found for {query}. Try a different subject or topic."
        
        tips = "🎯 Study Tips:\n\n"
        for i, result in enumerate(results[:3]):
            tips += f"• {result.get('title', 'Study tip')}\n"
            if result.get('snippet'):
                tips += f"  {result.get('snippet')}\n\n"
        
        return tips
    except Exception as e:
        return f"Error fetching study tips: {str(e)}"

def google_search_tool(query: str) -> str:
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        return "Missing SerpAPI key. Please set the SERPAPI_API_KEY environment variable."

    params = {
        "q": query,
        "api_key": api_key,
        "engine": "google",
        "num": 5
    }

    try:
        response = requests.get("https://serpapi.com/search", params=params)
        if response.status_code != 200:
            return f"Failed to fetch search results. Status code: {response.status_code}"

        data = response.json()
        results = data.get("organic_results", [])
        
        if not results:
            return "No search results found."
        
        formatted_results = []
        for i, result in enumerate(results[:5]):
            title = result.get('title', 'No title')
            link = result.get('link', 'No link')
            snippet = result.get('snippet', 'No description')
            formatted_results.append(f"{i+1}. **{title}**\n   {snippet}\n   URL: {link}")
        
        return "🔍 Search Results:\n\n" + "\n\n".join(formatted_results)
    except Exception as e:
        return f"Error performing search: {str(e)}"

def extract_video_id(video_input: str) -> str:
    if "youtube.com" in video_input or "youtu.be" in video_input:
        parsed_url = urlparse(video_input)
        if parsed_url.netloc == "youtu.be":
            return parsed_url.path.lstrip('/')
        elif parsed_url.netloc in ["www.youtube.com", "youtube.com"]:
            query_params = parse_qs(parsed_url.query)
            return query_params.get("v", [""])[0]
    else:
        # Assume it's already a video ID
        video_id_pattern = r'^[a-zA-Z0-9_-]{11}$'
        if re.match(video_id_pattern, video_input):
            return video_input
    
    return ""

def youtube_summary_tool(video_input: str) -> str:
    try:
        video_id = extract_video_id(video_input)
        
        if not video_id:
            return "Invalid YouTube video ID or URL. Please provide a valid YouTube video ID or URL."
        
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        if not transcript:
            return "No transcript available for this video."
        
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        full_text = " ".join([entry["text"] for entry in transcript])
        
        # Split into sentences and take the first 15-20 sentences
        sentences = re.split(r'[.!?]+', full_text)
        summary_text = ". ".join([s.strip() for s in sentences[:20] if s.strip()]) + "."
        
        return f"🎬 YouTube Video Summary:\n\nSource: {video_url}\n\n{summary_text}"
        
    except Exception as e:
        return f"Couldn't fetch or process YouTube transcript: {str(e)}"

def exam_strategy_tool(query: str) -> str:
    try:
        api_key = os.getenv("SERPAPI_API_KEY")
        if not api_key:
            return "Missing SerpAPI key. Please set the SERPAPI_API_KEY environment variable."
        
        search_query = f"exam strategies for {query}"
        params = {
            "q": search_query,
            "api_key": api_key,
            "engine": "google",
            "num": 5
        }
        
        response = requests.get("https://serpapi.com/search", params=params)
        if response.status_code != 200:
            return f"Failed to fetch exam strategies. Status code: {response.status_code}"
        
        data = response.json()
        results = data.get("organic_results", [])
        
        if not results:
            return f"No exam strategies found for {query}. Try a different exam type or subject."
        
        strategies = f"📘 Exam Strategies for {query}:\n\n"
        for i, result in enumerate(results[:5]):
            strategies += f"• {result.get('title', 'Strategy')}\n"
            if result.get('snippet'):
                strategies += f"  {result.get('snippet')}\n\n"
        
        return strategies
    except Exception as e:
        return f"Error fetching exam strategies: {str(e)}"

def flashcard_generator_tool(query: str) -> str:
    try:
        api_key = os.getenv("SERPAPI_API_KEY")
        if not api_key:
            return "Missing SerpAPI key. Please set the SERPAPI_API_KEY environment variable."
        
        search_query = f"key concepts {query} for flashcards"
        params = {
            "q": search_query,
            "api_key": api_key,
            "engine": "google",
            "num": 5
        }
        
        response = requests.get("https://serpapi.com/search", params=params)
        if response.status_code != 200:
            return f"Failed to fetch flashcard content. Status code: {response.status_code}"
        
        data = response.json()
        results = data.get("organic_results", [])
        
        if not results:
            return f"No content found for {query} flashcards. Try a different subject or topic."
        
        flashcards = f"📇 Flashcards for {query}:\n\n"
        for i, result in enumerate(results[:5]):
            title = result.get('title', f'Concept {i+1}')
            snippet = result.get('snippet', 'No description available')
            
            flashcards += f"**Card {i+1}**\nQ: What is {title.split(' - ')[0] if ' - ' in title else title}?\n"
            flashcards += f"A: {snippet}\n\n"
        
        return flashcards
    except Exception as e:
        return f"Error generating flashcards: {str(e)}"

def note_organizer_tool(query: str) -> str:
    try:
        api_key = os.getenv("SERPAPI_API_KEY")
        if not api_key:
            return "Missing SerpAPI key. Please set the SERPAPI_API_KEY environment variable."
        
        search_query = f"how to organize study notes for {query}"
        params = {
            "q": search_query,
            "api_key": api_key,
            "engine": "google",
            "num": 3
        }
        
        response = requests.get("https://serpapi.com/search", params=params)
        if response.status_code != 200:
            return f"Failed to fetch note organization tips. Status code: {response.status_code}"
        
        data = response.json()
        results = data.get("organic_results", [])
        
        if not results:
            return f"No note organization tips found for {query}. Try a different subject or topic."
        
        note_template = f"# 📝 Organized Study Notes for {query}\n\n"
        note_template += "## Key Concepts\n"
        
        for i, result in enumerate(results[:3]):
            title = result.get('title', f'Concept {i+1}')
            snippet = result.get('snippet', 'No information available')
            
            note_template += f"### {title.split(' - ')[0] if ' - ' in title else title}\n"
            note_template += f"{snippet}\n\n"
        
        note_template += "## Study Organization Tips\n"
        note_template += "- Create a study schedule with specific goals for each session\n"
        note_template += "- Use headings and subheadings to structure your notes\n"
        note_template += "- Review and revise notes regularly\n"
        note_template += "- Connect concepts with arrows or mind maps\n"
        note_template += "- Highlight key definitions and formulas\n\n"
        
        return note_template
    except Exception as e:
        return f"Error organizing notes: {str(e)}"

def concept_mapper_tool(query: str) -> str:
    try:
        api_key = os.getenv("SERPAPI_API_KEY")
        if not api_key:
            return "Missing SerpAPI key. Please set the SERPAPI_API_KEY environment variable."
        
        search_query = f"main concepts related to {query}"
        params = {
            "q": search_query,
            "api_key": api_key,
            "engine": "google",
            "num": 5
        }
        
        response = requests.get("https://serpapi.com/search", params=params)
        if response.status_code != 200:
            return f"Failed to fetch concept data. Status code: {response.status_code}"
        
        data = response.json()
        results = data.get("organic_results", [])
        
        if not results:
            return f"No concept data found for {query}. Try a different subject or topic."
        
        concept_map = f"🔄 Concept Map for {query}:\n\n"
        concept_map += f"## Central Concept: {query.upper()}\n\n"
        
        # Create branches of the concept map
        for i, result in enumerate(results[:5]):
            title = result.get('title', f'Related Concept {i+1}')
            snippet = result.get('snippet', 'No description available')
            
            concept_map += f"### Branch {i+1}: {title.split(' - ')[0] if ' - ' in title else title}\n"
            concept_map += f"{snippet[:150]}...\n\n"
        
        concept_map += "To create a visual concept map:\n"
        concept_map += "1. Place the central concept in the middle\n"
        concept_map += "2. Connect related concepts with lines\n"
        concept_map += "3. Add brief descriptions on the connecting lines\n"
        concept_map += "4. Use different colors for different categories of concepts\n"
        
        return concept_map
    except Exception as e:
        return f"Error creating concept map: {str(e)}"

def scholarly_papers_tool(query: str) -> str:
    try:
        api_key = os.getenv("SERPAPI_API_KEY")
        if not api_key:
            return "Missing SerpAPI key. Please set the SERPAPI_API_KEY environment variable."
        
        search_query = f"scholarly papers on {query}"
        params = {
            "q": search_query,
            "api_key": api_key,
            "engine": "google_scholar",
            "num": 5
        }
        
        response = requests.get("https://serpapi.com/search", params=params)
        if response.status_code != 200:
            return f"Failed to fetch scholarly papers. Status code: {response.status_code}"
        
        data = response.json()
        organic_results = data.get("organic_results", [])
        
        if not organic_results:
            return f"No scholarly papers found for {query}. Try a different academic topic."
        
        papers = f"📄 Scholarly Papers on {query}:\n\n"
        for i, result in enumerate(organic_results[:5]):
            title = result.get('title', f'Paper {i+1}')
            authors = result.get('publication_info', {}).get('authors', [])
            authors_text = ", ".join(authors) if authors else "Unknown authors"
            snippet = result.get('snippet', 'No abstract available')
            
            papers += f"**{i+1}. {title}**\n"
            papers += f"Authors: {authors_text}\n"
            papers += f"Abstract: {snippet}\n\n"
        
        return papers
    except Exception as e:
        return f"Error fetching scholarly papers: {str(e)}"

def subject_expert_tool(query: str) -> str:
    try:
        api_key = os.getenv("SERPAPI_API_KEY")
        if not api_key:
            return "Missing SerpAPI key. Please set the SERPAPI_API_KEY environment variable."
        
        subject = query.split()[0] if query.split() else "general"
        search_query = f"expert insights on {query}"
        
        params = {
            "q": search_query,
            "api_key": api_key,
            "engine": "google",
            "num": 3
        }
        
        response = requests.get("https://serpapi.com/search", params=params)
        if response.status_code != 200:
            return f"Failed to fetch expert insights. Status code: {response.status_code}"
        
        data = response.json()
        results = data.get("organic_results", [])
        
        if not results:
            return f"No expert insights found for {query}. Try a different subject or topic."
        
        expert_insights = f"🎓 Expert Insights on {query}:\n\n"
        
        for i, result in enumerate(results[:3]):
            title = result.get('title', f'Insight {i+1}')
            snippet = result.get('snippet', 'No information available')
            
            expert_insights += f"**Expert Point {i+1}**: {title}\n"
            expert_insights += f"{snippet}\n\n"
        
        expert_insights += "For deeper expertise, consider:\n"
        expert_insights += "- Consulting specialized textbooks\n"
        expert_insights += "- Finding subject-specific academic journals\n"
        expert_insights += "- Attending relevant webinars or lectures\n"
        
        return expert_insights
    except Exception as e:
        return f"Error connecting with subject experts: {str(e)}"