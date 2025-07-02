import numpy as np
import joblib
import os
from django.shortcuts import render
from django.http import JsonResponse

# Define the correct model path
MODEL_PATH = r"F:\projects\lung_cancer_app\predictor\models\tuned_xgb_model.pkl"

# Check if the model file exists before loading
if os.path.exists(MODEL_PATH):
    try:
        model = joblib.load(MODEL_PATH)
        print("✅ Model loaded successfully.")
    except Exception as e:
        model = None
        print(f"⚠️ ERROR: Model loading failed - {str(e)}")
else:
    model = None
    print(f"⚠️ WARNING: Model file not found at {MODEL_PATH}")

def homepage(request):
    """Render the homepage with the form."""
    return render(request, 'homepage.html')
def predict(request):
    """Handle form submission and predict lung cancer."""
    if request.method == 'POST':
        if model is None:
            return JsonResponse({'error': 'Model not loaded. Check the file path.'})

        try:
            # Extract form data with default values
            features = [
                'smoking', 'finger_discoloration', 'mental_stress', 'pollution', 'illness',
                'immune_weakness', 'breathing_issue', 'alcohol', 'throat_discomfort',
                'chest_tightness', 'family_history', 'smoking_family', 'stress_immune'
            ]

            # ✅ Convert checkboxes correctly: 'on' → 1, missing → 0
            input_data = [1 if request.POST.get(feature) == 'on' else 0 for feature in features]

            # ✅ Validate numeric inputs properly
            try:
                energy_level = float(request.POST.get('energy_level', 50))  # Default: 50
                oxygen_saturation = float(request.POST.get('oxygen_saturation', 95))  # Default: 95
            except ValueError:
                return JsonResponse({'error': 'Energy Level and Oxygen Saturation must be numbers.'}, status=400)

            # ✅ Ensure values are within valid range
            if not (1 <= energy_level <= 100) or not (50 <= oxygen_saturation <= 100):
                return JsonResponse({'error': 'Invalid values. Energy Level (1-100), Oxygen Saturation (50-100).'}, status=400)

            input_data.extend([energy_level, oxygen_saturation])

            # Convert to NumPy array
            input_array = np.array([input_data])

            # Make prediction
            prediction = model.predict(input_array)[0]
            result = "Lung Cancer Detected" if prediction == 1 else "No Lung Cancer"

            return JsonResponse({'result': result})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method. Use POST.'}, status=405)
