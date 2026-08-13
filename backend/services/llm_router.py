import os
import dspy
from google import genai as modern_genai
from openai import OpenAI

class LLMRouter:
    def __init__(self):
        # Determine global fallback provider if not specified
        self.active_provider = os.getenv("ACTIVE_LLM_PROVIDER", "GEMINI").strip().upper()
        
        # Keys
        self.gemini_keys = [k.strip() for k in (os.getenv("GEMINI_API_KEYS", "") or os.getenv("GEMINI_API_KEY", "")).split(",") if k.strip()]
        self.nim_api_key = os.getenv("NVIDIA_NIM_API_KEY", "")
        self.groq_api_key = os.getenv("GROQ_API_KEY", "")
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY", "")
        
        # Local endpoints
        self.ollama_model = os.getenv("OLLAMA_MODEL", "qwen3.5:4b")
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
        
        # Init Clients
        self.genai_clients = [modern_genai.Client(api_key=k) for k in self.gemini_keys] if self.gemini_keys else []
        self.ollama_client = OpenAI(base_url=self.ollama_base_url, api_key="ollama")
        
        self.groq_client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=self.groq_api_key) if self.groq_api_key else None
        self.openrouter_client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=self.openrouter_api_key) if self.openrouter_api_key else None
        self.nim_client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=self.nim_api_key) if self.nim_api_key else None

        print(f"LLMRouter Initialized. Default Fallback Provider: {self.active_provider}")

    def get_dspy_lm(self, provider: str = None, model: str = None):
        """Returns a configured dspy.LM object for the specified provider."""
        prov = (provider or self.active_provider).upper()
        
        if prov == "NIM" and self.nim_api_key:
            nim_model = model or os.getenv("NVIDIA_NIM_MODEL", "meta/llama-3.1-8b-instruct")
            return dspy.LM(f"openai/{nim_model}", api_key=self.nim_api_key, api_base="https://integrate.api.nvidia.com/v1", max_tokens=4096)
        
        elif prov == "OLLAMA":
            m = model or self.ollama_model
            return dspy.LM(model=f"openai/{m}", api_key="ollama", api_base=self.ollama_base_url, max_tokens=4096)
            
        elif prov == "GROQ" and self.groq_api_key:
            m = model or "llama-3.1-8b-instant"
            return dspy.LM(model=f"openai/{m}", api_key=self.groq_api_key, api_base="https://api.groq.com/openai/v1", max_tokens=4096)
            
        elif prov == "OPENROUTER" and self.openrouter_api_key:
            m = model or "meta-llama/llama-3.1-8b-instruct"
            return dspy.LM(model=f"openai/{m}", api_key=self.openrouter_api_key, api_base="https://openrouter.ai/api/v1", max_tokens=4096)
            
        else: # Default GEMINI
            api_key = self.gemini_keys[0] if self.gemini_keys else ""
            m = model or "gemini-2.5-flash"
            return dspy.LM(f"gemini/{m}", api_key=api_key, max_tokens=4096)

    def generate_content(self, prompt: str, system_instruction: str = "", provider: str = None, model: str = None) -> str:
        """Universal text generation function routing to specific provider."""
        prov = (provider or self.active_provider).upper()
        
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        try:
            if prov == "OLLAMA":
                m = model or self.ollama_model
                response = self.ollama_client.chat.completions.create(model=m, messages=messages, temperature=0.2, max_tokens=2048)
                return response.choices[0].message.content
                
            elif prov == "GROQ":
                if not self.groq_client: return "[Error] GROQ_API_KEY not set."
                m = model or "llama-3.1-8b-instant"
                response = self.groq_client.chat.completions.create(model=m, messages=messages, temperature=0.2, max_tokens=2048)
                return response.choices[0].message.content
                
            elif prov == "OPENROUTER":
                if not self.openrouter_client: return "[Error] OPENROUTER_API_KEY not set."
                m = model or "meta-llama/llama-3.1-8b-instruct"
                response = self.openrouter_client.chat.completions.create(model=m, messages=messages, temperature=0.2, max_tokens=2048)
                return response.choices[0].message.content
                
            elif prov == "NIM":
                if not self.nim_client: return "[Error] NVIDIA_NIM_API_KEY not set."
                m = model or os.getenv("NVIDIA_NIM_MODEL", "meta/llama-3.1-8b-instruct")
                response = self.nim_client.chat.completions.create(model=m, messages=messages, temperature=0.2, max_tokens=2048)
                return response.choices[0].message.content

            elif prov == "GEMINI":
                if not self.genai_clients: return "[Error] GEMINI_API_KEY not set."
                m = model or "gemini-2.5-flash"
                client = self.genai_clients[0]
                config = {}
                if system_instruction: config["system_instruction"] = system_instruction
                response = client.models.generate_content(model=m, contents=prompt, config=config)
                return response.text if response and response.text else ""
            
            else:
                return f"[Error] Unknown provider: {prov}"
                
        except Exception as e:
            print(f"{prov} Error: {e}")
            return ""

# Singleton instance
llm_router = LLMRouter()
