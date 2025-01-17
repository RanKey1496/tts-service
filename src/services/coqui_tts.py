import os
import torch
import torchaudio
import uuid
from config import ROOT_DIR
from utils import print_info, print_success, print_error
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts

class TTS:
    """
    Class for Text-to-Speech using Coqui TTS
    """
    
    def __init__(self, model_path, config_path) -> None:
        """
        Initialize the TTS class
        
        Returns:
            None
        """
        
        print_info("Loading TTS model...")
        config = XttsConfig()
        config.load_json(config_path)
        
        self._model = Xtts.init_from_config(config)
        self._model.load_checkpoint(config, checkpoint_dir = model_path, eval = True)
        print_success("TTS model loaded")
        
    def synthesize(self, text: str, speaker_wav: str, output_path: str = os.path.join(ROOT_DIR, "result")) -> str:
        """
        Synthesize text using the TTS model
        
        Args:
            text (str): Text to be synthesized
            speaker_wav (str): Speaker wav file
            output_file (str): Path to save the synthesized audio
        
        Returns:
            str: Path to the synthesized audio
        """
        
        if (len(text) > 390):
            print_error("Text too long, maximum length is 390 characters")
            return
        
        print_info("Computing speaker latents...")
        gpt_cond_latent, speaker_embedding = self._model.get_conditioning_latents(audio_path=speaker_wav)
        
        print_info("Synthesizing text...")
        output = self._model.inference(text, "es", gpt_cond_latent, speaker_embedding)
        
        output_file = os.path.join(output_path, f"{uuid.uuid4()}.wav")
        
        torchaudio.save(output_file, torch.tensor(output["wav"]).unsqueeze(0), 24000)
        
        print_success("Synthesized audio saved to {}".format(output_file))
        return output_file