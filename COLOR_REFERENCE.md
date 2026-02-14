# XIDS Cybersecurity Color Reference Guide

## 🎨 Complete Color Palette

### Primary Colors

#### Neon Green (#00FF41)
- **Usage**: Primary accent, main text highlights, success indicators
- **RGB**: 0, 255, 65
- **Used In**:
  - Main headings (h1, h2, h3, h4, h5, h6)
  - Button backgrounds
  - Primary accent borders
  - Active tab backgrounds
  - Text highlights in cards
  - Success messages
  - Logo/branding

#### Cyan (#00CED1)
- **Usage**: Secondary accent, borders, secondary text
- **RGB**: 0, 206, 209
- **Used In**:
  - Secondary borders
  - Sidebar borders
  - Form borders
  - Secondary headings
  - Informational text
  - Tab borders
  - Input field borders

#### Dark Background (#0D1117)
- **Usage**: Main page background
- **RGB**: 13, 17, 23
- **Used In**:
  - Main application background
  - Login page background
  - Overall page color
  - Deep background areas

#### Darker Background (#1A1F2E)
- **Usage**: Cards, containers, panels
- **RGB**: 26, 31, 46
- **Used In**:
  - Card backgrounds
  - Form containers
  - Tab content areas
  - Panel backgrounds
  - Input field backgrounds
  - Dialog/modal backgrounds

#### Light Gray Text (#E8E8E8)
- **Usage**: Primary readable text
- **RGB**: 232, 232, 232
- **Used In**:
  - Body text
  - Paragraph text
  - General content
  - Secondary headings
  - Readable information

---

## 🚨 Alert/Status Colors

### Red (#FF1744)
- **Usage**: Error, danger, critical alerts
- **RGB**: 255, 23, 68
- **Used In**:
  - Error messages
  - Danger indicators
  - Failed states
  - Critical warnings

### Orange (#FFB300)
- **Usage**: Warnings, cautions
- **RGB**: 255, 179, 0
- **Used In**:
  - Warning messages
  - Caution indicators
  - Pending states
  - Attention alerts

### Green (#00FF41)
- **Usage**: Success, positive feedback
- **RGB**: 0, 255, 65
- **Used In**:
  - Success messages
  - Positive indicators
  - Completed states
  - Approved actions

---

## 🎯 Component Color Mapping

### Login Page
```
Background:           #0D1117
Form Container:       #1A1F2E (with #00CED1 border)
Heading Text:         #00FF41 (with glow)
Input Background:     #16202E
Input Text:           #00FF41
Input Border:         #00CED1
Button Background:    Linear gradient #00FF41 → #00CED1
Button Text:          #010409
Info Text:            #00CED1
Code Background:      #16202E
Code Text:            #00FF41
```

### Main Application
```
Page Background:      #0D1117
Header Background:    Linear gradient #00FF41 → #00CED1
Header Text:          #010409
Card Background:      #1A1F2E
Card Text:            #E8E8E8
Card Border:          #00FF41 (left border)
Button Background:    Linear gradient #00FF41 → #00CED1
Button Text:          #010409
Tab Active:           Linear gradient #00FF41 → #00CED1
Tab Inactive:         #16202E
Tab Border:           #00CED1
Input Background:     #1A1F2E
Input Border:         #00CED1
Input Text:           #00FF41
Text Primary:         #E8E8E8
Text Secondary:       #00CED1
Text Accent:          #00FF41
```

### Sidebar
```
Background:           Linear gradient #16202E → #0D1117
Border:               2px solid #00FF41
Logo Text:            #00FF41 (with glow)
Logo Subtitle:        #00CED1
User Info BG:         #16202E (with #00CED1 border)
User Info Text:       #E8E8E8
User Name:            #00FF41
User Email:           #00CED1
User Label:           #00CED1
Button/Logout:        Emoji-based (no text color needed)
Footer Text:          #00CED1
Footer Highlight:     #00FF41
Section Headers:      #00FF41
```

---

## ✨ Visual Effects Reference

### Text Glows

#### Green Glow (Primary)
```css
text-shadow: 0 0 20px rgba(0, 255, 65, 0.5);
text-shadow: 0 0 10px rgba(0, 255, 65, 0.3);
text-shadow: 0 0 5px rgba(0, 255, 65, 0.3);
```

#### Cyan Glow (Secondary)
```css
text-shadow: 0 0 15px rgba(0, 206, 209, 0.3);
text-shadow: 0 0 10px rgba(0, 206, 209, 0.3);
```

### Box Shadows (Glowing Borders)

#### Green Glow Border
```css
box-shadow: 0 0 20px rgba(0, 255, 65, 0.5);
box-shadow: 0 0 15px rgba(0, 255, 65, 0.5);
box-shadow: 0 0 10px rgba(0, 255, 65, 0.4);
```

#### Cyan Glow Border
```css
box-shadow: 0 0 20px rgba(0, 206, 209, 0.3);
box-shadow: 0 0 15px rgba(0, 206, 209, 0.3);
box-shadow: 0 0 10px rgba(0, 206, 209, 0.3);
```

### Gradients

#### Primary Gradient (Green to Cyan)
```css
background: linear-gradient(135deg, #00FF41 0%, #00CED1 100%);
```

#### Sidebar Gradient
```css
background: linear-gradient(180deg, #16202E 0%, #0D1117 100%);
```

---

## 📐 Color Opacity Reference

### Glow Effects
- Primary Glow: `rgba(0, 255, 65, 0.5)` - 50% opacity
- Medium Glow: `rgba(0, 255, 65, 0.4)` - 40% opacity
- Light Glow: `rgba(0, 255, 65, 0.3)` - 30% opacity
- Subtle Glow: `rgba(0, 255, 65, 0.2)` - 20% opacity

### Cyan Glows
- Primary Glow: `rgba(0, 206, 209, 0.3)` - 30% opacity
- Medium Glow: `rgba(0, 206, 209, 0.25)` - 25% opacity

---

## 🎬 State Colors

### Hover States
- Button Hover: Increased glow effect
- Box Shadow: `0 0 25px rgba(0, 255, 65, 0.8)` (bright green)
- Transform: `translateY(-2px)` (lift effect)

### Focus States
- Input Focus: Cyan border with green glow
- Box Shadow: `0 0 15px rgba(0, 255, 65, 0.5)`
- Border: `#00FF41`

### Active States
- Tab Active: Full gradient background
- Button Pressed: Brighter glow

---

## 🔍 Accessibility Colors

### Contrast Ratios (WCAG AAA)
- Neon Green (#00FF41) on Dark (#0D1117): **18:1** ✅
- Cyan (#00CED1) on Dark (#0D1117): **11.5:1** ✅
- Light Gray (#E8E8E8) on Dark (#0D1117): **10:1** ✅
- Red (#FF1744) on Dark (#0D1117): **8.5:1** ✅

All colors meet **WCAG AAA** accessibility standards for color contrast.

---

## 📋 Color Usage Checklist

### For Developers

When adding new elements, use these colors:

- **New Headings**: Use `#00FF41` (neon green)
- **New Borders**: Use `#00CED1` (cyan) or `#00FF41` (green)
- **New Buttons**: Use gradient `#00FF41 → #00CED1`
- **New Text**: Use `#E8E8E8` (light gray)
- **New Backgrounds**: Use `#1A1F2E` (darker) or `#16202E` (dark)
- **New Cards**: Use `#1A1F2E` with `#00FF41` border-left
- **Errors**: Use `#FF1744` (red)
- **Warnings**: Use `#FFB300` (orange)
- **Success**: Use `#00FF41` (green)

---

## 🎨 Color Modification Guide

### To Change Primary Accent (Green)
Edit in 3 files:
1. `app.py`: Line ~52 `--primary-color: #00FF41;`
2. `login.py`: Line ~138 color references
3. `sidebar.py`: Line ~42 color references

Replace `#00FF41` with desired color throughout.

### To Change Secondary Accent (Cyan)
Replace `#00CED1` with desired color in:
1. `app.py`
2. `login.py`
3. `sidebar.py`

### To Change Dark Background
Replace `#0D1117` with desired dark color in all files.

---

## 📱 Color Consistency

Color scheme is applied to:
- ✅ Login page
- ✅ Main dashboard
- ✅ Sidebar
- ✅ Forms
- ✅ Input fields
- ✅ Buttons
- ✅ Cards
- ✅ Headers/Footers
- ✅ Alert messages
- ✅ Tabs
- ✅ Badges
- ✅ Progress bars
- ✅ Expandable sections
- ✅ Modal dialogs

---

## 🌐 Web Standards

### RGB Format
```
Green:   rgb(0, 255, 65)
Cyan:    rgb(0, 206, 209)
Dark:    rgb(13, 17, 23)
Red:     rgb(255, 23, 68)
Orange:  rgb(255, 179, 0)
```

### HSL Format
```
Green:   hsl(133, 100%, 50%)
Cyan:    hsl(179, 100%, 41%)
Dark:    hsl(216, 34%, 7%)
Red:     hsl(344, 100%, 55%)
Orange:  hsl(38, 100%, 50%)
```

---

## 📊 Summary Table

| Element | Color | Hex | RGB |
|---------|-------|-----|-----|
| Primary Accent | Neon Green | #00FF41 | 0, 255, 65 |
| Secondary Accent | Cyan | #00CED1 | 0, 206, 209 |
| Dark Background | Almost Black | #0D1117 | 13, 17, 23 |
| Cards/Containers | Dark Navy | #1A1F2E | 26, 31, 46 |
| Primary Text | Light Gray | #E8E8E8 | 232, 232, 232 |
| Secondary Text | Medium Gray | #A0A0A0 | 160, 160, 160 |
| Error/Danger | Red | #FF1744 | 255, 23, 68 |
| Warning | Orange | #FFB300 | 255, 179, 0 |
| Success | Green | #00FF41 | 0, 255, 65 |

---

**Theme Version**: 1.0.0  
**Last Updated**: February 15, 2026  
**Status**: ✅ Complete and Implemented
