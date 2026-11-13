import Link from "next/link";
export default function NotFound() {
  return (
    <div className="state-box">
      <h1>Page not found</h1>
      <p>Let’s get back to the next problem.</p>
      <Link className="button" href="/">
        Explore problems
      </Link>
    </div>
  );
}
