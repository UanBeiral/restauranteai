import { createClient } from "@supabase/supabase-js";

const supabaseUrl = "https://zabpentdalxkjdmezwse.supabase.co";
const supabaseAnonKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InphYnBlbnRkYWx4a2pkbWV6d3NlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDY0ODEzODgsImV4cCI6MjA2MjA1NzM4OH0.4SJYgmEu41S8H8avYEeVQF9jdYQH5Gd0ipIoM13VIPo";

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
