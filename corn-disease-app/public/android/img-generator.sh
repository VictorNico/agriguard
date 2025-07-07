#!/bin/bash

# Script pour générer toutes les icônes Android à partir d'une icône source
# Usage: ./generate_android_icons.sh icon_source.png

# Vérifier si le fichier source existe
if [ ! -f "$1" ]; then
    echo "❌ Erreur: Fichier source '$1' non trouvé"
    echo "Usage: $0 <chemin_vers_icone_source>"
    exit 1
fi

SOURCE_ICON="$1"
echo "🚀 Génération des icônes Android à partir de: $SOURCE_ICON"

# Créer les dossiers s'ils n'existent pas
mkdir -p res/mipmap-mdpi
mkdir -p res/mipmap-hdpi
mkdir -p res/mipmap-xhdpi
mkdir -p res/mipmap-xxhdpi
mkdir -p res/mipmap-xxxhdpi

# Générer les icônes principales (ic_launcher)
echo "📱 Génération des icônes principales..."
sips -Z 48 "$SOURCE_ICON" --out res/mipmap-mdpi/ic_launcher.png
sips -Z 72 "$SOURCE_ICON" --out res/mipmap-hdpi/ic_launcher.png
sips -Z 96 "$SOURCE_ICON" --out res/mipmap-xhdpi/ic_launcher.png
sips -Z 144 "$SOURCE_ICON" --out res/mipmap-xxhdpi/ic_launcher.png
sips -Z 192 "$SOURCE_ICON" --out res/mipmap-xxxhdpi/ic_launcher.png

# Générer les icônes rondes (ic_launcher_round)
echo "🔵 Génération des icônes rondes..."
sips -Z 48 "$SOURCE_ICON" --out res/mipmap-mdpi/ic_launcher_round.png
sips -Z 72 "$SOURCE_ICON" --out res/mipmap-hdpi/ic_launcher_round.png
sips -Z 96 "$SOURCE_ICON" --out res/mipmap-xhdpi/ic_launcher_round.png
sips -Z 144 "$SOURCE_ICON" --out res/mipmap-xxhdpi/ic_launcher_round.png
sips -Z 192 "$SOURCE_ICON" --out res/mipmap-xxxhdpi/ic_launcher_round.png

# Créer les dossiers pour les drawables
mkdir -p res/drawable-mdpi
mkdir -p res/drawable-hdpi
mkdir -p res/drawable-xhdpi
mkdir -p res/drawable-xxhdpi
mkdir -p res/drawable-xxxhdpi

# Générer les drawables (pour les icônes dans l'app)
echo "🎨 Génération des drawables..."
sips -Z 24 "$SOURCE_ICON" --out res/drawable-mdpi/ic_launcher.png
sips -Z 36 "$SOURCE_ICON" --out res/drawable-hdpi/ic_launcher.png
sips -Z 48 "$SOURCE_ICON" --out res/drawable-xhdpi/ic_launcher.png
sips -Z 72 "$SOURCE_ICON" --out res/drawable-xxhdpi/ic_launcher.png
sips -Z 96 "$SOURCE_ICON" --out res/drawable-xxxhdpi/ic_launcher.png

# Générer les icônes d'écran de démarrage (splash)
echo "🌟 Génération des icônes splash..."
mkdir -p res/drawable-land-mdpi
mkdir -p res/drawable-land-hdpi
mkdir -p res/drawable-land-xhdpi
mkdir -p res/drawable-land-xxhdpi
mkdir -p res/drawable-land-xxxhdpi

mkdir -p res/drawable-port-mdpi
mkdir -p res/drawable-port-hdpi
mkdir -p res/drawable-port-xhdpi
mkdir -p res/drawable-port-xxhdpi
mkdir -p res/drawable-port-xxxhdpi

# Splash landscape
sips -Z 200 "$SOURCE_ICON" --out res/drawable-land-mdpi/splash.png
sips -Z 300 "$SOURCE_ICON" --out res/drawable-land-hdpi/splash.png
sips -Z 400 "$SOURCE_ICON" --out res/drawable-land-xhdpi/splash.png
sips -Z 600 "$SOURCE_ICON" --out res/drawable-land-xxhdpi/splash.png
sips -Z 800 "$SOURCE_ICON" --out res/drawable-land-xxxhdpi/splash.png

# Splash portrait
sips -Z 200 "$SOURCE_ICON" --out res/drawable-port-mdpi/splash.png
sips -Z 300 "$SOURCE_ICON" --out res/drawable-port-hdpi/splash.png
sips -Z 400 "$SOURCE_ICON" --out res/drawable-port-xhdpi/splash.png
sips -Z 600 "$SOURCE_ICON" --out res/drawable-port-xxhdpi/splash.png
sips -Z 800 "$SOURCE_ICON" --out res/drawable-port-xxxhdpi/splash.png

# Créer les icônes adaptatives (Android 8.0+)
echo "🔄 Génération des icônes adaptatives..."
mkdir -p res/mipmap-anydpi-v26

# Fichiers XML pour les icônes adaptatives
cat > res/mipmap-anydpi-v26/ic_launcher.xml << 'EOF'
<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/ic_launcher_background"/>
    <foreground android:drawable="@mipmap/ic_launcher_foreground"/>
</adaptive-icon>
EOF

cat > res/mipmap-anydpi-v26/ic_launcher_round.xml << 'EOF'
<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/ic_launcher_background"/>
    <foreground android:drawable="@mipmap/ic_launcher_foreground"/>
</adaptive-icon>
EOF

# Générer les foregrounds pour les icônes adaptatives
echo "🎯 Génération des foregrounds adaptatifs..."
sips -Z 48 "$SOURCE_ICON" --out res/mipmap-mdpi/ic_launcher_foreground.png
sips -Z 72 "$SOURCE_ICON" --out res/mipmap-hdpi/ic_launcher_foreground.png
sips -Z 96 "$SOURCE_ICON" --out res/mipmap-xhdpi/ic_launcher_foreground.png
sips -Z 144 "$SOURCE_ICON" --out res/mipmap-xxhdpi/ic_launcher_foreground.png
sips -Z 192 "$SOURCE_ICON" --out res/mipmap-xxxhdpi/ic_launcher_foreground.png

# Créer le fichier colors.xml pour la couleur de fond
mkdir -p res/values
cat > res/values/colors.xml << 'EOF'
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="ic_launcher_background">#FFFFFF</color>
</resources>
EOF

echo "✅ Génération terminée!"
echo ""
echo "📊 Résumé des fichiers générés:"
echo "   • Icônes principales: 5 tailles (mdpi à xxxhdpi)"
echo "   • Icônes rondes: 5 tailles"
echo "   • Drawables: 5 tailles"
echo "   • Splash screens: 10 orientations x 5 tailles"
echo "   • Icônes adaptatives: Support Android 8.0+"
echo ""
echo "🔧 Prochaines étapes:"
echo "   1. Vérifiez les icônes générées dans le dossier 'res/'"
echo "   2. Ajustez la couleur de fond dans res/values/colors.xml"
echo "   3. Copiez les fichiers dans votre projet Android"
echo "   4. Testez sur différents appareils"
