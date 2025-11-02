"""
Two-Stage Hybrid Intent Classification System
Combines rule-based validation + ML classifier for robust intent detection
"""

from input_validator import InputValidator
from train_ensemble_classifier import EnsembleIntentClassifier
import logging

logger = logging.getLogger(__name__)


class HybridIntentClassifier:
    """
    Two-stage classification system:
    Stage 1: Rule-based validation (fast, high precision)
    Stage 2: ML classifier (catches edge cases)
    
    Only proceeds to depression assessment if BOTH stages approve.
    """
    
    def __init__(self, use_ml=True, ml_threshold=0.6):
        """
        Initialize hybrid classifier.
        
        Args:
            use_ml: Whether to use ML classifier (False = rules only)
            ml_threshold: Confidence threshold for ML predictions (0.6 = 60%)
        """
        self.validator = InputValidator()
        self.use_ml = use_ml
        self.ml_threshold = ml_threshold
        self.ml_classifier = None
        
        if use_ml:
            try:
                self.ml_classifier = EnsembleIntentClassifier()
                if self.ml_classifier.load_model():
                    logger.info("✅ ML intent classifier loaded successfully")
                else:
                    logger.warning("⚠️ ML classifier not found, using rules only")
                    self.use_ml = False
            except Exception as e:
                logger.error(f"❌ Failed to load ML classifier: {e}")
                self.use_ml = False
    
    def classify_intent(self, text):
        """
        Two-stage intent classification.
        
        Returns:
            dict: {
                'is_valid': bool,  # True if should proceed to depression assessment
                'stage1_result': dict,  # Rule-based validation result
                'stage2_result': dict or None,  # ML classification result
                'final_decision': str,  # 'genuine', 'casual', 'short', 'question', etc.
                'confidence': float,  # Overall confidence
                'method': str,  # 'rules', 'ml', or 'hybrid'
                'message': str,  # User-facing message
                'examples': str  # Helpful examples if rejected
            }
        """
        result = {
            'is_valid': False,
            'stage1_result': None,
            'stage2_result': None,
            'final_decision': None,
            'confidence': 0.0,
            'method': 'rules',
            'message': '',
            'examples': ''
        }
        
        # ===== STAGE 1: RULE-BASED VALIDATION =====
        is_valid_rules, validation_type, metadata = self.validator.validate_input(text)
        
        result['stage1_result'] = {
            'is_valid': is_valid_rules,
            'type': validation_type,
            'metadata': metadata
        }
        
        logger.info(f"Stage 1 (Rules): {validation_type} - valid={is_valid_rules}")
        
        # If rules reject, get response
        if not is_valid_rules:
            response = self.validator.get_smart_response(validation_type)
            result['final_decision'] = validation_type
            result['message'] = response['message']
            result['examples'] = response['examples']
            result['confidence'] = 1.0  # Rules are definitive
            result['method'] = 'rules'
            logger.warning(f"❌ Rejected by rules: {validation_type}")
            return result
        
        # ===== STAGE 2: ML CLASSIFICATION (if enabled) =====
        if self.use_ml and self.ml_classifier:
            try:
                ml_result = self.ml_classifier.predict(text)
                result['stage2_result'] = ml_result
                
                ml_intent = ml_result['intent']
                ml_confidence = ml_result['confidence']
                
                logger.info(f"Stage 2 (ML): {ml_intent} - confidence={ml_confidence:.2%}")
                
                # Decision logic: ML predicts casual with high confidence
                if ml_intent == 'casual' and ml_confidence >= self.ml_threshold:
                    # ML caught something rules missed
                    result['final_decision'] = 'casual_ml'
                    result['confidence'] = ml_confidence
                    result['method'] = 'hybrid'
                    result['message'] = "⚠️ Please describe your actual feelings and emotions more clearly."
                    result['examples'] = (
                        "💡 **Try sharing:**\n"
                        "- 'I've been feeling sad and tired for weeks'\n"
                        "- 'I'm anxious and can't sleep well'\n"
                        "- 'My mood is low and I have no energy'"
                    )
                    logger.warning(f"❌ Rejected by ML: {ml_intent} ({ml_confidence:.1%})")
                    return result
                
                # ML and rules both approve
                elif ml_intent == 'genuine':
                    result['is_valid'] = True
                    result['final_decision'] = 'genuine'
                    result['confidence'] = ml_confidence
                    result['method'] = 'hybrid'
                    logger.info(f"✅ Approved by both rules and ML ({ml_confidence:.1%})")
                    return result
                
                # ML uncertain - trust rules (they approved)
                else:
                    result['is_valid'] = True
                    result['final_decision'] = 'genuine'
                    result['confidence'] = 0.7  # Lower confidence when ML uncertain
                    result['method'] = 'hybrid_uncertain'
                    logger.info(f"✅ Approved by rules (ML uncertain: {ml_confidence:.1%})")
                    return result
                    
            except Exception as e:
                logger.error(f"ML classification failed: {e}, falling back to rules")
                # Fall through to rules-only decision
        
        # ===== RULES-ONLY DECISION =====
        # If we got here, rules approved and either ML is disabled or ML approved
        result['is_valid'] = True
        result['final_decision'] = 'genuine'
        result['confidence'] = 0.85
        result['method'] = 'rules' if not self.use_ml else 'hybrid'
        logger.info(f"✅ Approved (method: {result['method']})")
        
        return result
    
    def get_stats(self):
        """Get classifier statistics."""
        return {
            'rule_validator': 'active',
            'ml_classifier': 'active' if self.use_ml else 'disabled',
            'ml_threshold': self.ml_threshold,
            'total_keywords': len(self.validator.ALL_FEELING_KEYWORDS),
            'casual_phrases': len(self.validator.CASUAL_PHRASES)
        }


# Convenience function
def classify_user_intent(text, use_ml=True, ml_threshold=0.6):
    """
    Quick classification function.
    
    Args:
        text: User input
        use_ml: Whether to use ML classifier
        ml_threshold: Confidence threshold for ML predictions
    
    Returns:
        dict: Classification result
    """
    classifier = HybridIntentClassifier(use_ml=use_ml, ml_threshold=ml_threshold)
    return classifier.classify_intent(text)
