        <script type="text/javascript">
            
            "use strict";
            class TabsManual {
                /*
                *   This content is licensed according to the W3C Software License at
                *   https://www.w3.org/Consortium/Legal/2015/copyright-software-and-document
                *
                *   File:   tabs-manual.js
                *
                *   Desc:   Tablist widget that implements ARIA Authoring Practices
                */
                constructor(groupNode) {
                    this.tablistNode = groupNode;
                
                    this.tabs = [];
                
                    this.firstTab = null;
                    this.lastTab = null;
                
                    this.tabs = Array.from(this.tablistNode.querySelectorAll("[role=tab]"));
                    console.log(this.tabs)
                    this.tabpanels = [];
                
                    for (let i = 0; i < this.tabs.length; i += 1) {
                        const tab = this.tabs[i];
                        const tabpanel = document.getElementById (
                            tab.getAttribute("aria-controls")
                        );
                
                        tab.tabIndex = -1;
                        tab.setAttribute("aria-selected", "false");
                        this.tabpanels.push(tabpanel);
                        
                        tab.addEventListener("click", this.onClick.bind(this));
                    
                        if (!this.firstTab) {
                            this.firstTab = tab;
                        }
                        this.lastTab = tab;
                    }
                    console.log(this.tabpanels)
                    this.setSelectedTab(this.firstTab);
                }
            
                setSelectedTab(currentTab) {
                    for (let i = 0; i < this.tabs.length; i += 1) {
                        const tab = this.tabs[i];
                        if (currentTab === tab) {
                            tab.setAttribute("aria-selected", "true");
                            tab.removeAttribute("tabindex");
                            this.tabpanels[i].classList.remove("is-hidden");
                        } else {
                            tab.setAttribute("aria-selected", "false");
                            tab.tabIndex = -1;
                            this.tabpanels[i].classList.add("is-hidden");
                        }
                    }
                }

                /* EVENT HANDLERS */
                // Since this example uses buttons for the tabs, the click onr also is activated
                // with the space and enter keys
                onClick(event) {
                    //alert("salut");
                    this.setSelectedTab(event.currentTarget);
                }
            }
            
            class NavigareImagini {
                constructor(groupNode) {
                    
                    /* detectarea butoanelor de navigare imagini*/
                    this.btn_img_anterioara = document.querySelectorAll("[id=btn-imaginea-anterioara")[0];
                    this.btn_img_urmatoare = document.querySelectorAll("[id=btn-imaginea-urmatoare")[0];
                    console.log(this.btn_img_anterioara);
                    console.log(this.btn_img_urmatoare);
                    this.btn_img_anterioara.addEventListener("click", this.onClick.bind(this))
                    this.btn_img_urmatoare.addEventListener("click", this.onClick.bind(this))

                    /* initializare obiecte imagini */
                    this.grupPoze = groupNode;
                    this.poze = []

                    this.primaPoza = null;
                    this.ultimaPoza = null;
                    /* detectare imagini */
                    this.poze = Array.from(this.grupPoze.querySelectorAll("[role=img-etapa]"))
                    //console.log(this.poze)
                    for(let i = 0; i < this.poze.length; i += 1) {
                        const poza = this.poze[i]
                        console.log("poza:", poza)
                        poza.addEventListener("click", this.onClickPoza.bind(this))
                        if(this.primaPoza == null) {
                            this.primaPoza = poza;
                        }
                        this.ultimaPoza = poza;
                    }
                    this.pozaCurenta = this.primaPoza;
                }
                actiuneButon(obiectButon) {
                    console.log(obiectButon);
                    let indexPozaCurenta = this.poze.indexOf(this.pozaCurenta);
                    console.log(indexPozaCurenta);
                    if(obiectButon.id === "btn-imaginea-anterioara") {
                        this.btn_img_urmatoare.setAttribute("style", "background-color: initial")
                        if(this.pozaCurenta != this.primaPoza) {
                            //ascundem poza curenta
                            this.pozaCurenta.setAttribute("aria-selected", "false");
                            //selectam noua poza curenta
                            this.pozaCurenta = this.poze[indexPozaCurenta - 1];
                            this.pozaCurenta.setAttribute("aria-selected", "true");
                        } else {
                            obiectButon.setAttribute("style", "pointer-events: none; background-color: red;");
                        }
                    } else if(obiectButon.id === "btn-imaginea-urmatoare") {
                        this.btn_img_anterioara.setAttribute("style", "background-color: initial")
                        if(this.pozaCurenta != this.ultimaPoza) {
                            //ascundem poza curenta
                            this.pozaCurenta.setAttribute("aria-selected", "false");
                            //selectam noua poza curenta
                            this.pozaCurenta = this.poze[indexPozaCurenta + 1];
                            this.pozaCurenta.setAttribute("aria-selected", "true");
                        } else {
                            obiectButon.setAttribute("style", "pointer-events: none; background-color: red");
                        }
                    }
                    
                }
                onClick(event) {
                    this.actiuneButon(event.currentTarget)
                }
                onClickPoza(eveniment) {
                    console.log("Click pe poza:", eveniment.target);
                    console.log("img src:", eveniment.target.src)
                    const dialog = document.getElementById("dialog-modal");
                    
                    const div_dialog_modal = document.querySelector("#dialog-modal > div")
                    const elementImgInDialog = document.createElement("img");
                    elementImgInDialog.src = eveniment.target.src
                    //elementImgInDialog.setAttribute("style", "width:800px;")
                    div_dialog_modal.appendChild(elementImgInDialog);
                    
                    dialog.showModal();
                }
            }

            function inchideDialogModal() {
                let dialog_modal = document.getElementById("dialog-modal");
                const div_dialog_modal = document.querySelector("#dialog-modal > div")
                let imagine_in_dialog = document.querySelector("#dialog-modal > div > img");
                if(imagine_in_dialog) {
                    div_dialog_modal.removeChild(imagine_in_dialog);
                }
                dialog_modal.close()
            }

            // Initialize tablist
            
            window.addEventListener("load", function () {
                const tablists = document.querySelectorAll("[role=tablist].manual");
                console.log(tablists)
                for (let i = 0; i < tablists.length; i++) {
                    new TabsManual(tablists[i]);
                }
                const grup_poze_de_afisat = document.querySelectorAll("[role=grup-poze-de-afisat]")
                new NavigareImagini(grup_poze_de_afisat[0]);

                const buton_dialog_modal = document.querySelector("#dialog-modal > div > button")
                console.log("buton dialog modal:", buton_dialog_modal)
                buton_dialog_modal.addEventListener("click", inchideDialogModal)
            });
        </script>