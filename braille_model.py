from transformers import BertForMaskedLM, BertTokenizer
import torch
import numpy as np
from collections import defaultdict

class BrailleBERTModel:
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertForMaskedLM.from_pretrained('bert-base-uncased')
        self.model.eval()
        self.user_patterns = defaultdict(list)
    
    def predict(self, current_word, user_history):
        # Analyze user history for patterns
        context = self._analyze_user_patterns(user_history)
        
        # Create masked sentence
        masked_sentence = f"{context} {current_word} [MASK]."
        
        # Tokenize input
        tokenized = self.tokenizer(masked_sentence, return_tensors='pt')
        mask_position = (tokenized['input_ids'][0] == self.tokenizer.mask_token_id).nonzero().item()
        
        # Predict
        with torch.no_grad():
            output = self.model(**tokenized)
        
        # Get top predictions
        predictions = output.logits[0, mask_position].topk(5)
        predicted_tokens = [self.tokenizer.decode([idx]) for idx in predictions.indices]
        
        # Filter valid words
        valid_words = [word for word in predicted_tokens if word.isalpha() and len(word) > 1]
        
        return valid_words[:3]
    
    def update_model(self, original_word, corrected_word, user_id):
        # Store correction pattern for user
        self.user_patterns[user_id].append((original_word, corrected_word))
    
    def _analyze_user_patterns(self, user_history):
        # Simple pattern analysis - could be enhanced
        if not user_history:
            return ""
        
        # Get most frequent corrections
        corrections = defaultdict(int)
        for seq, norm, char, timestamp in user_history:
            # Simple pattern detection - could be enhanced
            pass
            
        return " ".join([f"User often types {wrong} as {right}" for wrong, right in corrections.items()][:2])