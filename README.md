# svg-creator-website

The project I am working on will be a Vue.js web application that will be used to create annotated SVGs for use as MIDI instruments, such as overlays for the Sensel Morph.

The website will consist of a selection of controls in a pane on the left, that will allow users to drag the shapes onto a canvas. These will be items such as buttons (pads) and sliders. The users will be able to change the dimensions of the controls, and the styles, such as colour.

The added functionality of this over a standard SVG creator will be the fact that this site will allow you to add additional information and metadata to the SVGs. This could be, for example, a MIDI stop command, or a specific note on a MIDI device. This site will have a list of these commands to choose from in a drop-down menu, making the creation of these layouts and overlays very accessible.

The users will be able to use a menu at the top of the screen to export the controls with their respective annotations. To begin with, this will simply allow the exportation of the SVG layouts, but could be expanded to allow the user to export to a Haskell text output.

A further stretch goal could be to allow the users to log in to save and edit their control schemes. Another could be to allow the upload of previously created control schemes for editing and further adaptation.

When paired with these devices, such as the Sensel Morph, this website will allow users to seamlessly create custom overlays and commands suited to their needs, ready for integration with the device.

# Color Scheme

The color scheme for this application is as follows:

`#000000` black

`#2F4550` charcoal

`#586F7C` dark electric blue

`#B8DBD9` powder blue

`#F4F4F9` ghost white

Error Message: `#EF476F` paradise pink

Warning Message: `#FFD166` orange yellow crayola

Success Message: `#06D6A0` carribbean green

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
