# Braille Auto-Correct System

A real-time Braille input system with intelligent auto-correction and BERT-based suggestions, designed for QWERTY keyboard users.

![System Demo](static/demo.gif) *(Optional: Add a demo GIF later)*

## Key Features

- **Six-Key Braille Input**: Type Braille using standard keyboard keys (D, W, Q, K, O, P)
- **Real-Time Auto-Correction**: Handles common input errors and typos
- **Context-Aware Suggestions**: BERT-powered word predictions
- **Learning Mechanism**: Improves suggestions based on user corrections
- **Accessible Interface**: Visual feedback with optional auditory cues

## How the Braille Input Works

### Key Mapping
| Braille Dot | Keyboard Key |
|-------------|-------------|
| Dot 1       | D           |
| Dot 2       | W           |
| Dot 3       | Q           |
| Dot 4       | K           |
| Dot 5       | O           |
| Dot 6       | P           |

### Input Mechanism
1. **Simultaneous Key Presses**: 
   - Press multiple keys together to form a Braille character
   - Example: `D + K` = Braille 'C' (dots 1 and 4)

2. **Sequence Handling**:
   - System detects key combinations when released
   - Order of key presses doesn't matter (`DK` = `KD`)

3. **Control Keys**:
   - `Space`: Word separation
   - `Backspace`: Delete character
   - `Enter`: New line

## Auto-Correction System

### Error Handling
1. **Extra/Missing Dots**:
   - `DKP` → Corrects to `DK` (ignores extra 'P')
   - `KQ` → Suggests `KQW` (common missing 'W')

2. **Common Mistakes**:
   - Predefined correction patterns (e.g., `DP` → `DQ`)
   - Dynamic learning from user corrections

3. **Visual Feedback**:
   - Corrected characters highlighted temporarily
   - Suggested words appear below cursor

### Suggestion Engine
1. **Two-Phase Approach**:
   - **Phase 1**: Fast pattern matching (Levenshtein distance)
   - **Phase 2**: Contextual BERT predictions

2. **Learning**:
   - Stores correction patterns per user
   - Adapts to individual typing habits

## System Architecture

```mermaid
graph TD
    A[Key Press Detection] --> B[Sequence Normalization]
    B --> C{Valid Braille?}
    C -->|Yes| D[Character Lookup]
    C -->|No| E[Closest Match]
    D --> F[Display Character]
    E --> F
    F --> G[Word Formation]
    G --> H{Word Complete?}
    H -->|Yes| I[Generate Suggestions]
    H -->|No| A
    I --> J[Display Suggestions]
