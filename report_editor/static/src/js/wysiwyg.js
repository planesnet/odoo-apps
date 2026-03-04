/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { Wysiwyg } from "@html_editor/wysiwyg";
import { _t } from "@web/core/l10n/translation";

patch(Wysiwyg.prototype, {
  getEditorConfig() {
    const config = super.getEditorConfig();

    config.resources = config.resources || {};
    if (!config.resources.user_commands) config.resources.user_commands = [];
    if (!config.resources.toolbar_items) config.resources.toolbar_items = [];

    config.resources.user_commands.push({
      id: "setLineHeight",
      description: _t("Interlineado"),
      icon: "fa-text-height",
      run: () => {
        const selection = window.getSelection();
        if (!selection || selection.rangeCount === 0) return;
        let node = selection.focusNode;

        if (node && node.nodeType === Node.TEXT_NODE) {
          node = node.parentNode;
        }

        const blockTags = [
          "P",
          "DIV",
          "LI",
          "TD",
          "TH",
          "H1",
          "H2",
          "H3",
          "H4",
          "H5",
          "H6",
        ];

        while (
          node &&
          node.tagName &&
          !blockTags.includes(node.tagName.toUpperCase())
        ) {
          if (node.classList?.contains("odoo-editor-editable")) {
            break;
          }
          node = node.parentNode;
        }

        if (!node) return;

        let currentHeight = node.style.lineHeight || "1.2";
        currentHeight = currentHeight
          .replace(" !important", "")
          .replace("important", "")
          .trim();

        const height = prompt("Interlineado (ej: 1, 1.5, 2.0):", currentHeight);
        if (!height) return;

        node.style.setProperty("line-height", height, "important");

        node.dispatchEvent(new Event("input", { bubbles: true }));
      },
    });

    config.resources.user_commands.push({
      id: "setParagraphSpacing",
      description: _t("Espaciado entre párrafos"),
      icon: "fa-arrows-v",
      run: () => {
        const selection = window.getSelection();
        if (!selection || selection.rangeCount === 0) return;

        let node = selection.focusNode;
        if (node && node.nodeType === Node.TEXT_NODE) node = node.parentNode;

        const blockTags = [
          "P",
          "DIV",
          "LI",
          "TD",
          "TH",
          "H1",
          "H2",
          "H3",
          "H4",
          "H5",
          "H6",
        ];
        while (
          node &&
          node.tagName &&
          !blockTags.includes(node.tagName.toUpperCase())
        ) {
          if (node.classList?.contains("odoo-editor-editable")) break;
          node = node.parentNode;
        }
        if (!node) return;

        let currentMargin = node.style.marginBottom || "0px";
        currentMargin = currentMargin
          .replace(" !important", "")
          .replace("important", "")
          .trim();

        const margin = prompt(
          "Espacio después del párrafo (ej: 10px, 1.5rem, 15px):",
          currentMargin,
        );
        if (!margin) return;

        node.style.setProperty("margin-bottom", margin, "important");
        node.dispatchEvent(new Event("input", { bubbles: true }));
      },
    });

    config.resources.toolbar_items.push({
      id: "line_height_button",
      groupId: "layout",
      commandId: "setLineHeight",
    });

    config.resources.toolbar_items.push({
      id: "paragraph_spacing_button",
      groupId: "layout",
      commandId: "setParagraphSpacing",
    });

    return config;
  },
});
