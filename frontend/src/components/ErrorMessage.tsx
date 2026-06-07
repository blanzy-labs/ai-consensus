type ErrorMessageProps = {
  message: string;
};

function ErrorMessage({ message }: ErrorMessageProps) {
  if (!message) {
    return null;
  }

  return (
    <section className="error-message" role="alert">
      {message}
    </section>
  );
}

export default ErrorMessage;
