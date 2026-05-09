const vscode = require("vscode");

function activate(context) {
  const disposable = vscode.commands.registerCommand("clinic.explainCode", async () => {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      vscode.window.showWarningMessage("No active editor");
      return;
    }

    const selection = editor.document.getText(editor.selection);
    if (!selection) {
      vscode.window.showWarningMessage("Select code first");
      return;
    }

    const panel = vscode.window.createWebviewPanel(
      "clinicCodeExplain",
      "Code Explanation",
      vscode.ViewColumn.Beside,
      {}
    );

    panel.webview.html = `<html><body><h2>Code explanation</h2><pre>${selection}</pre><p>This is a scaffold. AI call will be added in next steps.</p></body></html>`;
  });

  context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = { activate, deactivate };
