import type { ProviderName } from "../types/consensus";

const providers: ProviderName[] = ["openai", "gemini"];

type ModelSelectorProps = {
  id: string;
  label: string;
  value: ProviderName;
  disabled: boolean;
  onChange: (provider: ProviderName) => void;
};

function ModelSelector({ id, label, value, disabled, onChange }: ModelSelectorProps) {
  return (
    <label className="field">
      <span>{label}</span>
      <select
        id={id}
        value={value}
        disabled={disabled}
        onChange={(event) => onChange(event.target.value as ProviderName)}
      >
        {providers.map((provider) => (
          <option key={provider} value={provider}>
            {provider}
          </option>
        ))}
      </select>
    </label>
  );
}

export default ModelSelector;
