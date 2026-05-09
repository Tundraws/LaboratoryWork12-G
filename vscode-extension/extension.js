const vscode = require("vscode");

async function explainCode(code, customPrompt) {
  const config = vscode.workspace.getConfiguration("clinicCodeExplainer");
  const apiKey = config.get("apiKey");
  const model = config.get("model") || "deepseek-v4-flash";
  const endpoint = config.get("endpoint") || "https://api.deepseek.com/chat/completions";

  if (!apiKey) {
    throw new Error("Set clinicCodeExplainer.apiKey to a DeepSeek API key in VS Code settings.");
  }

  const prompt = customPrompt || "Explain this code in simple words for a junior developer.";
  const response = await fetch(endpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      model,
      messages: [
        { role: "system", content: "You are a helpful code tutor." },
        { role: "user", content: `${prompt}\n\n${code}` },
      ],
      temperature: 0.2,
    }),
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(`AI request failed: ${body}`);
  }

  const data = await response.json();
  return data.choices?.[0]?.message?.content || "No explanation generated.";
}

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

    const customPrompt = await vscode.window.showInputBox({
      placeHolder: "Optional custom prompt (leave empty for default)",
      prompt: "Prompt for AI explanation",
    });

    let explanation = "";
    try {
      explanation = await explainCode(selection, customPrompt);
    } catch (error) {
      vscode.window.showErrorMessage(String(error));
      return;
    }

    const panel = vscode.window.createWebviewPanel(
      "clinicCodeExplain",
      "Code Explanation",
      vscode.ViewColumn.Beside,
      {}
    );

    panel.webview.html = `
      <html>
        <body>
          <h2>Explanation</h2>
          <pre style="white-space: pre-wrap;">${explanation.replace(/</g, "&lt;").replace(/>/g, "&gt;")}</pre>
        </body>
      </html>
    `;
  });

  context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = { activate, deactivate };
