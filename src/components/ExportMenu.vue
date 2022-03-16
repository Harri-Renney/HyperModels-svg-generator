<template>
    <div class="sign-up-form">
        <div class="form-container">
            <div class="menu">
                <div class="welcome-message">
                    <span class="title">Export Layout</span><br/>
                    Enter the filename below...
                </div>
                <div class="item text">
                    <input required type="text" id="filename" v-model="filename" placeholder="MyLayout1.svg">
                </div>

                <div class="item button" @click="exportCanvas">
                    Export
                </div>

                <div class="item skip" @click="closeExportMenu">
                    <span class="skip">Cancel Export</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { saveAs } from 'file-saver'
import $ from 'jquery'
export default {
    name: 'ExportMenu',
    data() {
        return {
            filename: '',
        }
    },
    methods: {
        closeExportMenu() {
            this.$emit('close-export-menu')
        },
        hexToRgb(hex) {
            var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
            return result ? "rgb(" + parseInt(result[1], 16) + "," + parseInt(result[2], 16) + "," + parseInt(result[3], 16) + ")" : null;
        },
        exportCanvas() {
            if (this.filename == '') {
                alert('You must enter filename')
                return
            }

            var json = JSON.parse(this.$parent.$root.$refs.canvas.exportCanvasToJson())
            console.log(json)
            var device = this.$parent.$root.$refs.canvas.device

            var svg = ""

            if(device.name == "custom")
            {
                //@ToDo - make it use the chosen dimension units, like px, mm.
                // svg = "<svg xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' height='" + 
                //     (device.height) + "px' viewbox='0 0 " + (device.height) + " " + 
                //     (device.width) + "' width='"  + (device.width) + 
                //     "px' version='1.11.1' interface_device='" + device.name + "'>"
                console.log(device.height)
                console.log(device.height)
                svg = "<svg xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' height='" + 
                    (device.height) + "' viewbox='0 0 " + (device.height) + " " + 
                    (device.width) + "' width='"  + (device.width) + 
                    "' version='1.11.1' interface_device='" + device.name + "'>"
            }
            else{
                svg = "<svg xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' height='" + 
                    (device ? device.height / 50 : 20) + "mm' viewbox='0 0 " + (device ? device.height / 50 : 20) + " " + 
                    (device ? device.width / 50 : 20) + "' width='"  + (device ? device.width / 50 : 20) + 
                    "mm' version='1.11.1' interface_device='" + device.name + "'>"
            }

            let fullPhyiscsEq = ""
            json.objects.forEach((control) => {

                fullPhyiscsEq += control.physicsKernel + "\n";
                console.log(control.physicsKernel);
            })

            console.log(fullPhyiscsEq)

            // @Highlight - Generate physics kernel from equations.
            let generatedCode =  fullPhyiscsEq;
            $.ajax({
                type: "POST",
                url: "http://127.0.0.1:5000/parse",
                async: false,
                data: { mydata: generatedCode },
                success: function(data) {
                    //<!-- do something here -->
                    generatedCode = data.name;
                }
            });
            console.log(generatedCode)
            
            json.objects.forEach((control) => {
                //var physicsKernelBase64 = btoa(control.physicsKernel)
                var physicsKernelBase64 = btoa(generatedCode)
                switch (control.type) {
                    // @Highlight - Added another parameter into SVG here for phyiscs Equation.
                    case 'rect':
                        if (control.inter_type == 'pad') {
                            //@ToDo - Is this incorporating scaling somehow? For unit types, not sure, but may be useful to implement it.
                            // svg += "<" + control.type + " interface_osc_address='" + control.inter_osc_address + "' interface_type='" + control.inter_type +
                            // "' interface_osc_args='" + control.inter_osc_args + "' width='" + Math.round((control.width / 50) * control.scaleX) + "' height='" + 
                            // Math.round((control.height / 50) * control.scaleY) + "' x='" + ((control.left - 200) / 50) + "' y='" + ((control.top - 50) / 50) + 
                            // "' style='fill:" + this.hexToRgb(control.fill) + ";' physics_kernel='" +  physicsKernelBase64 + "'/>"
                            svg += "<" + control.type + " interface_osc_address='" + control.inter_osc_address + "' interface_type='" + control.inter_type +
                            "' interface_osc_args='" + control.inter_osc_args + "' width='" + (control.width * control.scaleX) + "' height='" + 
                            (control.height * control.scaleY) + "' x='" + control.left + "' y='" + control.top + 
                            "' style='fill:" + this.hexToRgb(control.fill) + ";' physics_kernel='" +  physicsKernelBase64 + "'/>"
                        }
                        if (control.inter_type.endsWith("_slider")) {
                            svg += "<" + control.type + " interface_osc_address='" + control.inter_osc_address + "' interface_type='" + control.inter_type + 
                            "' interface_osc_args='" + control.inter_osc_args + "' width='" + Math.round((control.width / 50) * control.scaleX) + "' height='" + 
                            Math.round((control.height / 50) * control.scaleY) + "' x='" + ((control.left - 200) / 50) + "' y='" + ((control.top - 50) / 50) + 
                            "' style='fill:" + this.hexToRgb(control.fill) + ";' max='" + control.max + "' min='" + control.min + "' init='" + control.init + 
                            "' incr='" + control.incr + "' physics_kernel='" +  physicsKernelBase64 +  "'/>"
                        }
                        break
                    case 'circle':
                        // svg += "<" + control.type + " interface_osc_address='" + control.inter_osc_address + "' interface_type='" + control.inter_type +
                        //     "' interface_osc_args='" + control.inter_osc_args + "'r='" + (control.radius / 50) * control.scaleX + "' cx='" + 
                        // ((control.left - 200 + (control.strokeWidth / 2)) + (control.radius * control.scaleX)) / 50 + "' cy='" + ((control.top - 50 + 
                        // (control.strokeWidth / 2)) + (control.radius * control.scaleY)) / 50 + "' style='fill:" + (this.hexToRgb(control.fill) ?? 'rgba(0, 0, 0, 0)') + ";stroke-width:" +
                        // control.strokeWidth / 50 + ";stroke:" + control.stroke + "' physics_kernel='" +  physicsKernelBase64 +  "'/>"
                        svg += "<" + control.type + " interface_osc_address='" + control.inter_osc_address + "' interface_type='" + control.inter_type +
                            "' interface_osc_args='" + control.inter_osc_args + "' r='" + control.radius + "' cx='" + 
                        (control.left + control.radius) + "' cy='" + (control.top + (control.radius)) + "' physics_kernel='" +  physicsKernelBase64 +  "'/>"
                        break
                    // case 'ellipse':
                    //     svg += "<ellipse rx='" + (control.radius / 50) * control.scaleX + "' ry='" + (control.radius / 50) * control.scaleY + "' cx='" + 
                    //     ((control.left - 200 + (control.strokeWidth / 2)) + (control.radius * control.scaleX)) / 50 + "' cy='" + ((control.top - 50 + 
                    //     (control.strokeWidth / 2)) + (control.radius * control.scaleY)) / 50 + "' style='fill:" + (this.hexToRgb(control.fill) ?? 'rgba(0, 0, 0, 0)') + ";stroke-width:" +
                    //     control.strokeWidth / 50 + ";stroke:" + control.stroke + "' physics_kernel='" +  physicsKernelBase64 + "'></ellipse>"
                    case 'path':
                    {
                        // svg += "<" + control.type + " interface_osc_address='" + control.inter_osc_address + "' interface_type='" + control.inter_type +
                        //     "' interface_osc_args='" + control.inter_osc_args + "'r='" + (control.radius / 50) * control.scaleX + "' cx='" + 
                        // ((control.left - 200 + (control.strokeWidth / 2)) + (control.radius * control.scaleX)) / 50 + "' cy='" + ((control.top - 50 + 
                        // (control.strokeWidth / 2)) + (control.radius * control.scaleY)) / 50 + "' style='fill:" + (this.hexToRgb(control.fill) ?? 'rgba(0, 0, 0, 0)') + ";stroke-width:" +
                        // control.strokeWidth / 50 + ";stroke:" + control.stroke + "' physics_kernel='" +  physicsKernelBase64 +  "'/>"
                        console.log("line coords: " + control.path[0][0] + " " + control.path[0][1] + 
                            " " + control.path[0][2] + " " + control.path[1][0] + " " + control.path[1][1] + " " + control.path[1][2])
                        console.log("Line scale: " + control.scaleX + " " + control.scaleY)
                        console.log("Line pos: " + control.top + " " + control.left)
                        let x1 = control.left
                        let x2 = ((control.path[1][1] - control.path[0][1]) * control.scaleX) + control.left
                        let y1 = control.top
                        let y2 = control.top
                        svg += "<path interface_osc_address='" + control.inter_osc_address + "' interface_type='" + control.inter_type +
                            "' interface_osc_args='" + control.inter_osc_args + "' d='" + control.path[0][0] + " " + x1 + 
                            " " + y1 + " " + control.path[1][0] + " " + x2 + " " + y2 + "' physics_kernel='" +  
                            physicsKernelBase64 +  "'/>"
                        break
                    }
                }
            })


            svg += "</svg>"

            var blob = new Blob([svg], {type: "image/svg+xml"})

            saveAs.saveAs(blob, (this.filename.endsWith('.svg') ? this.filename : this.filename + ".svg"))
        }
    }
}
</script>

<style scoped>

.form-container {
    width: 100%;
    top: 20%;
    position: absolute;
    margin-left: auto;
    margin-right: auto;
}

.sign-up-form {
    position: absolute;
    height: 100%;
    width: 100%;
    background-color: #00000055;
    z-index: 200;
}

.menu {
    max-width: 35%;
    background-color: #F4F4F9;
    border: solid #B8DBD9 3px;
    border-radius: 2px;
    z-index: 200;
    margin-left: auto;
    margin-right: auto
}

.item {
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 10px;
    width: 65%;
}

input {
    width: 100%;
    box-sizing: border-box;
    padding: 5px;
    height: 35px;
    outline: none;
    background-color: #F4F4F9;
    border: none;
    font-size: 20px;
    margin-left: auto;
    margin-right: auto;
}

input:focus {
    border-bottom: 2px #586F7C solid;
}

.button {
    text-align: center; 
    border: 2px black solid;
    width: 49%;
    margin: auto;
    border-bottom: 4px black solid;
    cursor: pointer;
}

.welcome-message {
    margin-left: auto;
    margin-right: auto;
    line-height: 50px;
    position: relative;
    left: 10px;
    font-weight: bold;
    font-size: 25px;
    color: #586F7C;
    text-align: center;
}

.title {
    color: #2F4550;
}

.text {
    border-bottom: 2px black solid;
}

div .skip {
    text-align: center;
    color: #586F7C;
    margin-top: 10px;
    cursor: pointer;
}

div .skip :hover {
    color: #B8DBD9;
}

span .skip {
    width: 100%;
    box-sizing: border-box;
    height: 35px;
    outline: none;
    border: none;
    font-size: 15px;
    display: inline-block;
}

.required {
    color: #EF476F;
    float: left;
}

#submit {
    cursor: pointer;
}
</style>
