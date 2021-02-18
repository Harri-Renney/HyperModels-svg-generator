<template>
    <div id="canvas" class="canvas">
        <canvas id="c"></canvas>
    </div>
</template>

<script>
import { fabric } from 'fabric'
export default {
    name: 'Canvas',
    data() {
        return {
            canvas_height: 0,
            canvas_width: 0,
            canvas: null,
            device: null,
            objects: []
        }
    },
    mounted() {
        this.canvas_height = window.innerHeight
        this.canvas_width = window.innerWidth - 250

        this.drawGrid()
    },
    props: {
        custom_size: Object
    },
    watch: {
        custom_size: function (newVal, oldVal) {
            console.log(oldVal)
            this.drawCustomDevice(newVal.custom_width, newVal.custom_height)
        }
    },
    methods: {
        changeDevice(device) {
            switch(device) {
                case "sensel-morph":
                    this.drawSenselMorph()
                    break
                case "roli-lightpad-block":
                    this.drawRoliLightpadBlock()
                    break
                case "custom":
                    this.showCustomSizeForm()
                    break
                case "none":
                default:
                    this.clearDevice()
                    break
            }
            this.objects.forEach(object => this.canvas.bringToFront(object.object))
        },
        drawSenselMorph() {
            this.clearDevice()
            // Sensel Morph is 23cm x 13cm | 1 grid sqaure is 1cm
            this.addSquare(23 * 50, 13 * 50, true)
        },
        drawRoliLightpadBlock() {
            this.clearDevice()
            // Roli Lightpad Block is 15 LEDs x 15 LEDs | 1 grid square is 1 LED
            this.addSquare(15 * 50, 15 * 50, true)
        },
        showCustomSizeForm() {
            this.$emit('show-custom-size-form')
        },
        drawCustomDevice(width, height) {
            this.addSquare(width * 50, height * 50, true)
        },
        clearDevice() {
            this.canvas.remove(this.device)
        },
        drawGrid() {
            var canvas =  new fabric.Canvas('c', { selection: false })
            canvas.setHeight(this.canvas_height)
            canvas.setWidth(this.canvas_width)
            var grid = 50

            for (var i = 0; i < (this.canvas_width / grid); i++) {
                canvas.add(new fabric.Line([i * grid, 0, i * grid, this.canvas_height], { stroke: '#ccc', selectable: false }))
                canvas.add(new fabric.Line([ 0, i * grid, this.canvas_width, i * grid], { stroke: '#ccc', selectable: false }))
            }
            
            canvas.on('object:moving', function(options) {
                console.log(canvas.getObjects().indexOf(options.target))
                options.target.set({
                    left: Math.round(options.target.left / grid) * grid,
                    top: Math.round(options.target.top / grid) * grid
                })
            })
            
            this.canvas = canvas

            const helperObj = new fabric.Object({})    //abstract invisible object
            helperObj.set("selectable", false)         //so the user is not able to select and modify it manually
            this.canvas.add(helperObj)

            this.canvas.on("object:added", () => {
                //workaround - selecting all objects to enable object controls

                let objects = this.canvas.getObjects()
                var selection = new fabric.ActiveSelection(objects, {
                    canvas: this.canvas,
                })
                this.canvas.setActiveObject(selection)   //selecting all objects...
                this.canvas.discardActiveObject()        //...and deselecting them
                this.canvas.requestRenderAll()
            })
        },
        addSquare(width = 100, height = 100, device = false) {
            var square = new fabric.Rect({
                left: 200,
                top: 100,
                width: width,
                height: height,
                fill: !device ? '#' + Math.floor(Math.random()*16777215).toString(16) : 'rgba(0, 0, 0, 0)',
                stroke: '#' + Math.floor(Math.random()*16777215).toString(16),
                strokeWidth: 5,
                strokeUniform: true,
                originX: 'left',
                originY: 'top',
                evented: true,
                transparentCorners: false,
                cornerStyle: 'circle',
                hasRotatingPoint: false,
                selectable: !device,
            })

            square.setControlsVisibility({
                mtr: false,
            })

            this.canvas.add(square)

            if (!device) {
                this.canvas.setActiveObject(square)
                this.objects.push({'shape': 'square', 'object': square})
            } else {
                square.hoverCursor = 'default'
                this.device = square
            }

            this.canvas.renderAll()
        },
        addCircle(width = 50, height = 50) {
            var circle = new fabric.Circle({
                left: 200,
                top: 200,
                width: width,
                height: height,
                fill: '#' + Math.floor(Math.random()*16777215).toString(16),
                stroke: '#' + Math.floor(Math.random()*16777215).toString(16),
                strokeWidth: 5,
                strokeUniform: true,
                originX: "left",
                originY: "top",
                evented: true,
                transparentCorners: false,
                cornerStyle: 'circle',
                radius: 50,
                hasRotatingPoint: false,
            })

            circle.setControlsVisibility({
                mtr: false,
            })

            this.canvas.add(circle)
            this.objects.push({'shape': 'circle', 'object': circle})

            this.canvas.renderAll()
        }
    }
}
</script>

<style scoped>

.canvas {
    position: absolute;
    left: 250px;
    top: 50px;
}
</style>