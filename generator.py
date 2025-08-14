import base64
import os
import re
from typing import Tuple, Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from openai import OpenAI


class DXFGenerator:
    """
    DXF Generator using OpenRouter API for image to CAD conversion
    """
    
    def __init__(self):
        self.base_url = os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.default_model = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
        self.max_tokens = int(os.getenv("DXF_MAX_TOKENS", "16384"))
        
        if not self.api_key:
            raise RuntimeError(
                "Missing OPENROUTER_API_KEY environment variable. "
                "Please set it in your environment or .env file."
            )
    
    def _get_client(self) -> OpenAI:
        """Get OpenAI client configured for OpenRouter"""
        return OpenAI(base_url=self.base_url, api_key=self.api_key)
    
    def _get_system_prompt(self, quality: str = "balanced") -> str:
        """Get system prompt based on quality setting"""
        base_prompt = (
            "You are a CAD DXF generator. Convert the provided 2D plan image into a valid ASCII DXF. "
            "Output only raw DXF text, no explanations, no markdown, no code fences. "
            "Requirements: start with '0\\nSECTION' and end with '0\\nEOF'. "
            "Use only DXF entities like LINE, LWPOLYLINE, and TEXT. "
            "Put geometry on layer WALLS and labels on layer TEXT. "
            "Absolutely do not include any prose."
        )
        
        quality_additions = {
            "fast": "Use simple approximations for speed. Focus on major structural elements.",
            "balanced": "Use consistent approximate scale. Balance accuracy with processing speed.",
            "high": "Use precise measurements when possible. Include detailed elements and annotations."
        }
        
        return base_prompt + " " + quality_additions.get(quality, quality_additions["balanced"])
    
    def _get_user_prompt(self, text_recognition: bool = True) -> str:
        """Get user prompt based on settings"""
        base_prompt = (
            "Trace the visible walls/rooms/labels from this floor plan image into straight segments"
        )
        
        if text_recognition:
            base_prompt += " and text. Include room labels and dimensions where visible."
        else:
            base_prompt += ". Focus only on structural elements, ignore text."
        
        base_prompt += " Return only raw ASCII DXF content (AutoCAD-compatible). Do not include any commentary or code fences."
        
        return base_prompt
    
    def _extract_dxf(self, text: str) -> str:
        """Extract clean DXF content from LLM response"""
        if not text:
            return ""
        
        # If fenced, keep the first fenced block that looks like DXF
        if "```" in text:
            blocks = re.findall(r"```[a-zA-Z0-9_-]*\n(.*?)```", text, flags=re.S)
            for block in blocks:
                if "SECTION" in block and "EOF" in block:
                    text = block
                    break
            else:
                # No valid fenced block found, remove all fences
                text = text.replace("```", "")
        
        data = text.strip()
        
        # Cut preamble before first SECTION
        start = data.find("0\nSECTION")
        if start != -1:
            data = data[start:]
        
        # Truncate after last EOF
        last_eof = data.rfind("0\nEOF")
        if last_eof != -1:
            data = data[:last_eof + len("0\nEOF")]
        
        return data.strip()
    
    def _validate_dxf(self, data: str) -> bool:
        """Validate if the data looks like a proper DXF file"""
        return bool(
            data and 
            data.startswith("0\nSECTION") and 
            "ENTITIES" in data and 
            data.endswith("0\nEOF")
        )
    
    def generate_dxf_from_image_bytes(
        self, 
        image_bytes: bytes, 
        config: Optional[dict] = None
    ) -> Tuple[str, str, bool, dict]:
        """
        Generate DXF from image bytes
        
        Args:
            image_bytes: Raw image data
            config: Configuration dictionary with settings
            
        Returns:
            Tuple of (dxf_content, raw_content, is_valid, metadata)
        """
        if config is None:
            config = {}
        
        # Extract configuration
        quality = config.get('quality', 'balanced')
        text_recognition = config.get('text_recognition', 'on') == 'on'
        model = config.get('model', self.default_model)
        
        # Encode image
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        
        # Prepare prompts
        system_prompt = self._get_system_prompt(quality)
        user_prompt = self._get_user_prompt(text_recognition)
        
        # Make API call
        client = self._get_client()
        
        try:
            completion = client.chat.completions.create(
                model=model,
                temperature=0.1,
                max_tokens=self.max_tokens,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": user_prompt},
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}
                            },
                        ],
                    },
                ],
            )
            
            raw_content = completion.choices[0].message.content or ""
            dxf_content = self._extract_dxf(raw_content)
            is_valid = self._validate_dxf(dxf_content)
            
            # Metadata for tracking
            metadata = {
                'model_used': model,
                'quality_setting': quality,
                'text_recognition': text_recognition,
                'tokens_used': completion.usage.total_tokens if completion.usage else 0,
                'processing_successful': bool(dxf_content),
                'validation_passed': is_valid
            }
            
            return dxf_content, raw_content, is_valid, metadata
            
        except Exception as e:
            # Return error information
            error_metadata = {
                'error': str(e),
                'model_used': model,
                'quality_setting': quality,
                'processing_successful': False,
                'validation_passed': False
            }
            return "", str(e), False, error_metadata


# Global instance for easy import
dxf_generator = DXFGenerator()
