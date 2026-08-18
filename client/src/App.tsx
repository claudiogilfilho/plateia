import { Toaster } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import NotFound from "@/pages/NotFound";
import { Route, Switch } from "wouter";
import type { ReactNode } from "react";
import DashboardLayout from "./components/DashboardLayout";
import ErrorBoundary from "./components/ErrorBoundary";
import { ThemeProvider } from "./contexts/ThemeContext";
import Dashboard from "./pages/Dashboard";
import History from "./pages/History";
import Home from "./pages/Home";
import InstagramConnection from "./pages/InstagramConnection";
import NewEvaluation from "./pages/NewEvaluation";
import Report from "./pages/Report";

function AppShell({ children }: { children: ReactNode }) {
  return <DashboardLayout>{children}</DashboardLayout>;
}

function Router() {
  return (
    <Switch>
      <Route path="/" component={Home} />
      <Route path="/app"><AppShell><Dashboard /></AppShell></Route>
      <Route path="/avaliar"><AppShell><NewEvaluation /></AppShell></Route>
      <Route path="/historico"><AppShell><History /></AppShell></Route>
      <Route path="/instagram"><AppShell><InstagramConnection /></AppShell></Route>
      <Route path="/analises/:id"><AppShell><Report /></AppShell></Route>
      <Route path="/404" component={NotFound} />
      <Route component={NotFound} />
    </Switch>
  );
}

function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider defaultTheme="light">
        <TooltipProvider>
          <Toaster />
          <Router />
        </TooltipProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
}

export default App;
