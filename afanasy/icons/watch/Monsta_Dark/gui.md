# Monsta Dark Theme - Color Reference

## UI Base Colors
| Setting | Hex | RGBA | Description | GUI Usage |
|---------|-----|------|-------------|-----------|
| clr_Window | #0A0A0A | rgba(10, 10, 10, 1) | Near Black | Main window background color |
| clr_WindowText | #CCCCCC | rgba(204, 204, 204, 1) | Light Gray | Default text color in windows |
| clr_DisabledText | #808070 | rgba(128, 128, 112, 1) | Muted Gray-Olive | Grayed out/disabled text |
| clr_Base | #9D9D9D | rgba(157, 157, 157, 1) | Medium Gray | Input fields, text boxes background |
| clr_Text | #CCCCCC | rgba(204, 204, 204, 1) | Light Gray | Text in input fields |
| clr_Button | #222222 | rgba(34, 34, 34, 1) | Very Dark Gray | Button background color |
| clr_Light | #666666 | rgba(102, 102, 102, 1) | Medium Gray | 3D effect light edge (top/left) |
| clr_Midlight | #555555 | rgba(85, 85, 85, 1) | Medium Gray | 3D effect mid-light |
| clr_Mid | #333333 | rgba(51, 51, 51, 1) | Dark Gray | 3D effect mid tone |
| clr_Dark | #222222 | rgba(34, 34, 34, 1) | Very Dark Gray | 3D effect dark edge (bottom/right) |
| clr_Shadow | #111111 | rgba(17, 17, 17, 1) | Near Black | Drop shadows, deepest 3D edge |

## Accent Colors
| Setting | Hex | RGBA | Description | GUI Usage |
|---------|-----|------|-------------|-----------|
| clr_Highlight | #A37333 | rgba(163, 115, 51, 1) | Golden Brown | Selection highlight background |
| clr_HighlightedText | #FFFFFF | rgba(255, 255, 255, 1) | White | Text color when selected |
| clr_Link | #402010 | rgba(64, 32, 16, 1) | Dark Brown | Hyperlink color |
| clr_LinkVisited | #CAFFB9 | rgba(202, 255, 185, 1) | Pale Green | Visited hyperlink color |

## Item Colors
| Setting | Hex | RGBA | Description | GUI Usage |
|---------|-----|------|-------------|-----------|
| clr_item | #828282 | rgba(130, 130, 130, 1) | Medium Gray | Default item background in lists |
| clr_selected | #B5B5B5 | rgba(181, 181, 181, 1) | Light Gray | Selected item background |
| clr_itemjob | #657652 | rgba(101, 118, 82, 1) | Muted Green | Active job item background |
| clr_itemjoboff | #474747 | rgba(71, 71, 71, 1) | Dark Gray | Offline/paused job background |
| clr_itemjobwtime | #477777 | rgba(71, 119, 119, 1) | Teal Gray | Job waiting for time background |
| clr_itemjobwdep | #61546E | rgba(97, 84, 110, 1) | Muted Purple | Job waiting for dependency background |
| clr_itemjobdone | #51FFFF | rgba(81, 255, 255, 1) | Cyan | Completed job background |
| clr_itemjoberror | #7F6550 | rgba(127, 101, 80, 1) | Brown Gray | Job with errors background |
| clr_itemrender | #637666 | rgba(99, 118, 102, 1) | Gray Green | Online render node background |
| clr_itemrenderoff | #50544C | rgba(80, 84, 76, 1) | Dark Olive Gray | Offline render node background |
| clr_itemrenderbusy | #667D55 | rgba(102, 125, 85, 1) | Muted Green | Busy/working render node background |
| clr_itemrenderpltclr | #DADA32 | rgba(218, 218, 50, 1) | Golden Yellow | Render node plotter/graph color |

## Status/State Colors
| Setting | Hex | RGBA | Description | GUI Usage |
|---------|-----|------|-------------|-----------|
| clr_running | #F89900 | rgba(248, 153, 0, 1) | Orange | Rendering progress bar color |
| clr_done | #184C4C | rgba(24, 76, 76, 1) | Dark Teal | Completed progress bar color |
| clr_error | #FA320A | rgba(250, 50, 10, 1) | Bright Red-Orange | Error indicator, failed tasks |
| clr_star | #F1CB0A | rgba(241, 203, 10, 1) | Gold Yellow | Star/priority indicator fill |

## UI Detail Colors
| Setting | Hex | RGBA | Description | GUI Usage |
|---------|-----|------|-------------|-----------|
| clr_outline | #515151 | rgba(81, 81, 81, 1) | Dark Gray | Item borders and outlines |
| clr_starline | #FFFFFF | rgba(255, 255, 255, 1) | White | Star/priority indicator outline |
| clr_textbright | #E2E2E2 | rgba(226, 226, 226, 1) | Light Gray | Bright/emphasized text |
| clr_textmuted | #5A5A5A | rgba(90, 90, 90, 1) | Medium Gray | Secondary/muted text |
| clr_textdone | #E3E3E3 | rgba(227, 227, 227, 1) | Light Gray | Text for completed items |
| clr_textstars | #323232 | rgba(50, 50, 50, 1) | Dark Gray | Text inside star indicators |

## Theme Settings
| Setting | Value | Description |
|---------|-------|-------------|
| theme | Monsta Dark | Theme display name |
| image_back | monsta.png | Background image file |
| font_family | SansSerif | Font family for UI |
| font_sizename | 10 | Font size for item names |
| font_sizeinfo | 8 | Font size for info text |
| font_sizemin | 5 | Minimum font size |
| font_sizeplotter | 7 | Font size in graph/plotter |
| star_numpoints | 5 | Number of star points |
| star_radiusout | 100 | Star outer radius |
| star_radiusin | 50 | Star inner radius |
| star_rotate | 10 | Star rotation angle |