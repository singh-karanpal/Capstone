library("shiny")
library("shinydashboard")
library("wordcloud")
library("SnowballC")
library("RColorBrewer")
library("tm")
library("readxl")
library("tidytext")
library("textdata")
library("wordcloud")
library("readxl")
library("tidyverse")
library("tidyr")
library("tokenizers")
library("igraph")
library("ggraph")
library("shinycssloaders")
library("magrittr")
library("stringr")
library("data.table")
library("Hmisc")
library("sentimentr")

# function for issue plotting over years
issue_plot <- function(result, token1, token2) {
  agg <-
    result %>% group_by(Year) %>% summarise(count = n()) %>% 
    mutate(per = paste(round(count / sum(count), 2) * 100, '%'))
  
  cw1 <- capitalize(token1)
  cw2 <- capitalize(token2)
  
  title <-
    bquote(paste(bold(.(cw1)) ~ bold(.(cw2)) ~ "Concern Over Years"))
  
  ggplot(agg, aes(x = as.factor(Year), y = per)) +
    geom_bar(stat = 'identity' , fill = "steelblue") +
    geom_text(aes(label = per),
              vjust = 1.6,
              color = "white",
              size = 5) +
    ggtitle(label = title) +
    ylab(label = 'Responses') +
    xlab(label = 'Years') +
    theme_minimal()
}

# function for sentiment highlight
plot_sentiment <- function(result, file_name) {
  df <- result
  
  feedbacks <-
    df %>% select(Comment) %>% mutate(id = row_number())
  group_df <-
    feedbacks %>% get_sentences(feedbacks$Comment) %>% select(Comment, id)
  
  sent_df <-
    sentiment(df$Comment) %>% select(element_id, sentiment)
  
  highlight_df <-
    cbind(group_df, sent_df) %>% select(sentiment, Comment, id)
  
  highlight_df %>% mutate(review = get_sentences(Comment)) %$% sentiment_by(review, id) %>% 
    highlight(file = file_name, open = FALSE)
}


# Dashboard Code
ui <- dashboardPage(
  # header
  dashboardHeader(title = 'BC Stats - Text Analytics', titleWidth = '15%'),
  
  #sidebar content
  dashboardSidebar(
    sidebarMenu(
      id = 'tab',
      menuItem('Concerns',
               tabName = 'q1',
               icon =  icon('chart-bar')),
      menuItem(
        'Appreciations',
        tabName = 'q2',
        icon = icon('chart-bar')
      ),
      menuItem(
        'Comparison',
        tabName = 'comparison',
        icon = icon('project-diagram')
      )
    ),
    collapsed = TRUE
  ),
  
  
  #body content
  dashboardBody(tags$script(HTML(
    "$('body').addClass('fixed');"
  )),
  tabItems(
    # 1st tab
    tabItem(
      tabName = 'q1',
      
      fluidRow(# ministry selector
        box(
          title = 'Select Ministries',
          selectizeInput(
            'ministry_names',
            label = NULL,
            choices = NULL,
            multiple = TRUE,
            options = list(create = TRUE),
          ),
          width = 12
        )),
      
      fluidRow(
        #Total Records
        valueBoxOutput('total_records', width = 3)  %>% withSpinner(color =
                                                                      "skyblue"),
        # 2013
        valueBoxOutput('records_2k13', width = 3),
        
        # 2018
        valueBoxOutput('records_2k18', width = 3),
        
        # 2020
        valueBoxOutput('records_2k20', width = 3)
      ),
      
      fluidRow(
        box(
          title = 'Employee Concerns',
          plotOutput('plot_wc') %>% withSpinner(color = "skyblue")
        ),
        box(
          title = 'Polarity',
          plotOutput('plot_pn') %>% withSpinner(color = "skyblue")
        )
      ),
      
      fluidRow(
        box(
          title = 'Markov Chain Text Processing',
          plotOutput('plot_mc') %>% withSpinner(color = "skyblue"),
          width = 8,
          height = 550
        ),
        box(
          title = 'Markov Threshold',
          sliderInput("slider_mc", "Minimum Occurrences:", 1, 600, 60),
          box(
            title = 'Entity Analysis',
            collapsible = TRUE,
            collapsed = TRUE,
            status = 'primary',
            solidHeader = TRUE,
            textInput(
              "text_word1",
              label = h5("From Token"),
              value = '',
              width = '50%'
            ),
            textInput(
              "text_word2",
              label = h5("To Token"),
              value = '',
              width = '50%'
            ),
            checkboxGroupInput(
              "checkGroup_ea",
              label = h3("Mining Options"),
              choices = list(
                "Issues Over Time" = 1,
                "Sentiment Highlights" = 2
              ),
              selected = ''
            ),
            width = 12
          )
          ,
          width = 4
        )
      ),
      
      
      fluidRow(
        class = "flex-nowrap",
        
        box(
          title = 'Issues Over Years',
          plotOutput('plot_issue') %>% withSpinner(color = "skyblue"),
          width = 4,
          collapsible = TRUE,
          collapsed = TRUE
        ),
        
        box(
          title = 'Sentiment Analysis',
          htmlOutput('sentiment'),
          width = 8,
          collapsible = TRUE,
          collapsed = TRUE
        )
      )
    ),
    
    
    # 2nd tab
    tabItem(
      tabName = 'q2',
      fluidRow(# ministry selector
        box(
          title = 'Select Ministries',
          selectizeInput(
            'ministry_names_q2',
            label = NULL,
            choices = NULL,
            multiple = TRUE,
            options = list(create = TRUE),
          ),
          width = 12
        )),
      
      fluidRow(
        #Total Records
        valueBoxOutput('total_records_q2', width = 3)  %>% withSpinner(color =
                                                                         "skyblue"),
        # 2013
        valueBoxOutput('records_2k13_q2', width = 3),
        
        # 2018
        valueBoxOutput('records_2k18_q2', width = 3),
        
        # 2020
        valueBoxOutput('records_2k20_q2', width = 3)
      ),
      
      fluidRow(
        box(
          title = 'Employee Concerns',
          plotOutput('plot_wc_q2') %>% withSpinner(color = "skyblue")
        ),
        box(
          title = 'Polarity',
          plotOutput('plot_pn_q2') %>% withSpinner(color = "skyblue")
        )
      ),
      
      fluidRow(
        box(
          title = 'Markov Chain Text Processing',
          plotOutput('plot_mc_q2') %>% withSpinner(color = "skyblue"),
          width = 8,
          height = 550
        ),
        box(
          title = 'Markov Threshold',
          sliderInput("slider_mc_q2", "Minimum Occurrences:", 1, 600, 25),
          box(
            title = 'Entity Analysis',
            collapsible = TRUE,
            collapsed = TRUE,
            status = 'primary',
            solidHeader = TRUE,
            textInput(
              "text_word1_q2",
              label = h5("From Token"),
              value = '',
              width = '50%'
            ),
            textInput(
              "text_word2_q2",
              label = h5("To Token"),
              value = '',
              width = '50%'
            ),
            checkboxGroupInput(
              "checkGroup_ea_q2",
              label = h3("Mining Options"),
              choices = list(
                "Issues Over Time" = 1,
                "Sentiment Highlights" = 2
              ),
              selected = ''
            ),
            width = 12
          )
          ,
          width = 4
        )
      ),
      
      
      fluidRow(
        class = "flex-nowrap",
        
        box(
          title = 'Issues Over Years',
          plotOutput('plot_issue_q2') %>% withSpinner(color = "skyblue"),
          width = 4,
          collapsible = TRUE,
          collapsed = TRUE
        ),
        
        box(
          title = 'Sentiment Analysis',
          htmlOutput('sentiment_q2'),
          width = 8,
          collapsible = TRUE,
          collapsed = TRUE
        )
      )
    )
  ))
)

server <- function(input, output, comments, session) {
  # setting seed
  set.seed(1234)
  
  # loading raw data
  data_df_q1 <-
    read_excel('../../data/interim/question1_models/ministries_Q1.xlsx')
  # loading raw data
  data_df_q2 <-
    read_excel('../../data/interim/question2_models/ministries_Q2.xlsx')
  
  
  ## checking which tab is active
  observe({
    tabs <- input$tab
    
    if (input$tab == 'q1') {
      # creating new objects for transformations
      comments <- data_df_q1
      only_comments <- comments %>% select(Comment)
      
      # updating selector with ministry names
      ministries <-
        comments %>% select(Ministry) %>% filter(Ministry != 'NA') %>% unique()
      updateSelectizeInput(
        session,
        'ministry_names',
        choices = sort(ministries$Ministry),
        server = TRUE
      )
      
      # updating dashboard according to ministries
      observe({
        user_filter <- input$ministry_names
        
        if (length(user_filter) != 0) {
          comments <- data_df_q1 %>% filter(Ministry %in% user_filter)
          only_comments <-
            comments %>% filter(Ministry %in% user_filter) %>% select(Comment)
          smry <-
            comments %>% filter(Ministry %in% user_filter) %>% group_by(Year) %>% 
              summarise(count = n())
          
        }
        else{
          comments <- data_df_q1
          only_comments <- comments %>% select(Comment)
          smry <-
            comments %>% group_by(Year) %>% summarise(count = n())
        }
        
        #Updating Data Stats
        #Total Records
        output$total_records <- renderValueBox({
          valueBox(
            nrow(only_comments),
            "Total Respondents",
            icon = icon("poll"),
            color = "purple"
          )
        })
        
        
        # 2013 Records
        output$records_2k13 <- renderValueBox({
          valueBox(smry$count[1],
                   "2013",
                   icon = icon("users"),
                   color = "orange")
        })
        
        # 2018 Records
        output$records_2k18 <- renderValueBox({
          valueBox(smry$count[2],
                   "2018",
                   icon = icon("users"),
                   color = "yellow")
        })
        
        # 2020 Records
        output$records_2k20 <- renderValueBox({
          valueBox(smry$count[3],
                   "2020",
                   icon = icon("users"),
                   color = "aqua")
        })
        
        
        # Text Mining
        single_tokens <-
          only_comments %>% unnest_tokens(word, Comment)
        
        bing_word_counts <- single_tokens %>%
          inner_join(get_sentiments("bing")) %>%
          count(word, sentiment, sort = TRUE) %>%
          ungroup()
        
        
        # Word Cloud Plot
        output$plot_wc <- renderPlot({
          # VERSION - Tidy
          plot <- single_tokens %>%
            anti_join(stop_words) %>%
            count(word) %>%
            with(
              wordcloud(
                word,
                n,
                max.words = 100,
                random.order = FALSE,
                rot.per = 0.35,
                colors = brewer.pal(8, "Dark2")
              )
            )
          
        })
        
        # New Plot - Polarity
        output$plot_pn <- renderPlot({
          bing_word_counts %>%
            group_by(sentiment) %>%
            top_n(10) %>%
            ungroup() %>%
            mutate(word = reorder(word, n)) %>%
            ggplot(aes(word, n, fill = sentiment)) +
            geom_col(show.legend = FALSE) +
            facet_wrap( ~ sentiment, scales = "free_y") +
            labs(y = "Contribution to sentiment",
                 x = NULL) +
            coord_flip() +
            theme_minimal()
        })
        
        # New Plot - Markov Chain Text Processing
        bigrams <-
          only_comments %>% mutate(line = row_number()) %>% 
            unnest_tokens(bigrams, Comment, token = 'ngrams', n = 2)
        
        bigrams_separated <- bigrams %>%
          separate(bigrams, c("word1", "word2"), sep = " ")
        
        bigrams_filtered <- bigrams_separated %>%
          filter(!word1 %in% stop_words$word) %>%
          filter(!word2 %in% stop_words$word)
        
        # new bigram counts:
        bigram_counts <- bigrams_filtered %>%
          count(word1, word2, sort = TRUE)
        
        bigram_counts <- bigram_counts %>% filter(!is.na(word1))
        
        # Plotting Markov Chains
        output$plot_mc <- renderPlot({
          bigram_graph <- bigram_counts %>%
            filter(n > input$slider_mc) %>%
            graph_from_data_frame()
          
          a <-
            grid::arrow(type = "closed", length = unit(.15, "inches"))
          
          ggraph(bigram_graph, layout = "fr") +
            geom_edge_link(
              aes(edge_alpha = n),
              show.legend = FALSE,
              arrow = a,
              end_cap = circle(.07, 'inches')
            ) +
            geom_node_point(color = "lightblue", size = 6) +
            geom_node_text(aes(label = name),
                           vjust = 1,
                           hjust = 1) +
            theme_void()
        })
        
        # Entity Analysis - Option Checking
        observeEvent(input$checkGroup_ea, {
          len <- length(input$checkGroup_ea)
          val <- input$checkGroup_ea
          
          token1 <- input$text_word1
          token2 <- input$text_word2
          search_word <- paste(token1, token2)
          result <-
            comments[comments$Comment %like% search_word, ] %>% select(Comment, Year)
          
          # Plotting Issues & Highlights
          if (len == 2) {
            # issues
            output$plot_issue <- renderPlot({
              issue_plot(result, token1, token2)
              
            })
            
            # sentiment
            plot_sentiment(result, 'highlight.html')
            
            getPage <- function() {
              return(includeHTML("highlight.html"))
            }
            
            output$sentiment <- renderUI({
              #getPage()
              tags$iframe(
                srcdoc = paste(readLines('highlight.html'), collapse = '\n'),
                width = "100%",
                height = "600px",
                frameborder = "0"
              )
            })
          }
          
          else if (len == 1 & val == 1) {
            output$plot_issue <- renderPlot({
              issue_plot(result, token1, token2)
              
            })
          }
          
          else if (len == 1 & val == 2) {
            plot_sentiment(result, 'highlight.html')
            
            getPage <- function() {
              return(includeHTML("highlight.html"))
            }
            
            output$sentiment <- renderUI({
              #getPage()
              tags$iframe(
                srcdoc = paste(readLines('highlight.html'), collapse = '\n'),
                width = "100%",
                height = "600px",
                frameborder = "0"
              )
            })
          }
          
        })
        
      }) # updating dashboard code ends here
      
    }
    else if (input$tab == 'q2') {
      # creating new objects for transformations
      comments <- data_df_q2
      only_comments <- comments %>% select(Comment)
      
      # updating selector with ministry names
      ministries <-
        comments %>% select(Ministry) %>% filter(Ministry != 'NA') %>% unique()
      updateSelectizeInput(
        session,
        'ministry_names_q2',
        choices = sort(ministries$Ministry),
        server = TRUE
      )
      
      # updating dashboard according to ministries
      observe({
        user_filter <- input$ministry_names_q2
        
        if (length(user_filter) != 0) {
          comments <- data_df_q2 %>% filter(Ministry %in% user_filter)
          only_comments <-
            comments %>% filter(Ministry %in% user_filter) %>% select(Comment)
          smry <-
            comments %>% filter(Ministry %in% user_filter) %>% group_by(Year) %>% summarise(count = n())
          
        }
        else{
          comments <- data_df_q2
          only_comments <- comments %>% select(Comment)
          smry <-
            comments %>% group_by(Year) %>% summarise(count = n())
        }
        
        #Updating Data Stats
        #Total Records
        output$total_records_q2 <- renderValueBox({
          valueBox(
            nrow(only_comments),
            "Total Respondents",
            icon = icon("poll"),
            color = "purple"
          )
        })
        
        
        # 2013 Records
        output$records_2k13_q2 <- renderValueBox({
          valueBox(smry$count[1],
                   "2013",
                   icon = icon("users"),
                   color = "orange")
        })
        
        # 2018 Records
        output$records_2k18_q2 <- renderValueBox({
          valueBox(smry$count[2],
                   "2018",
                   icon = icon("users"),
                   color = "yellow")
        })
        
        # 2020 Records
        output$records_2k20_q2 <- renderValueBox({
          valueBox(smry$count[3],
                   "2020",
                   icon = icon("users"),
                   color = "aqua")
        })
        
        
        # Text Mining
        single_tokens <-
          only_comments %>% unnest_tokens(word, Comment)
        
        bing_word_counts <- single_tokens %>%
          inner_join(get_sentiments("bing")) %>%
          count(word, sentiment, sort = TRUE) %>%
          ungroup()
        
        
        # Word Cloud Plot
        output$plot_wc_q2 <- renderPlot({
          # VERSION - Tidy
          plot <- single_tokens %>%
            anti_join(stop_words) %>%
            count(word) %>%
            with(
              wordcloud(
                word,
                n,
                max.words = 100,
                random.order = FALSE,
                rot.per = 0.35,
                colors = brewer.pal(8, "Dark2")
              )
            )
          
        })
        
        # New Plot - Polarity
        output$plot_pn_q2 <- renderPlot({
          bing_word_counts %>%
            group_by(sentiment) %>%
            top_n(10) %>%
            ungroup() %>%
            mutate(word = reorder(word, n)) %>%
            ggplot(aes(word, n, fill = sentiment)) +
            geom_col(show.legend = FALSE) +
            facet_wrap( ~ sentiment, scales = "free_y") +
            labs(y = "Contribution to sentiment",
                 x = NULL) +
            coord_flip() +
            theme_minimal()
        })
        
        # New Plot - Markov Chain Text Processing
        bigrams <-
          only_comments %>% mutate(line = row_number()) %>% 
          unnest_tokens(bigrams, Comment, token = 'ngrams', n = 2)
        
        bigrams_separated <- bigrams %>%
          separate(bigrams, c("word1", "word2"), sep = " ")
        
        bigrams_filtered <- bigrams_separated %>%
          filter(!word1 %in% stop_words$word) %>%
          filter(!word2 %in% stop_words$word)
        
        # new bigram counts:
        bigram_counts <- bigrams_filtered %>%
          count(word1, word2, sort = TRUE)
        
        bigram_counts <- bigram_counts %>% filter(!is.na(word1))
        
        # Plotting Markov Chains
        output$plot_mc_q2 <- renderPlot({
          bigram_graph <- bigram_counts %>%
            filter(n > input$slider_mc_q2) %>%
            graph_from_data_frame()
          
          a <-
            grid::arrow(type = "closed", length = unit(.15, "inches"))
          
          ggraph(bigram_graph, layout = "fr") +
            geom_edge_link(
              aes(edge_alpha = n),
              show.legend = FALSE,
              arrow = a,
              end_cap = circle(.07, 'inches')
            ) +
            geom_node_point(color = "lightblue", size = 6) +
            geom_node_text(aes(label = name),
                           vjust = 1,
                           hjust = 1) +
            theme_void()
        })
        
        # Entity Analysis - Option Checking
        observeEvent(input$checkGroup_ea_q2, {
          len <- length(input$checkGroup_ea_q2)
          val <- input$checkGroup_ea_q2
          
          token1 <- input$text_word1_q2
          token2 <- input$text_word2_q2
          search_word <- paste(token1, token2)
          result <-
            comments[comments$Comment %like% search_word, ] %>% select(Comment, Year)
          
          # Plotting Issues & Highlights
          if (len == 2) {
            # issues
            output$plot_issue_q2 <- renderPlot({
              issue_plot(result, token1, token2)
              
            })
            
            # sentiment
            plot_sentiment(result, 'highlight_q2.html')
            
            getPage <- function() {
              return(includeHTML("highlight_q2.html"))
            }
            
            output$sentiment_q2 <- renderUI({
              #getPage()
              tags$iframe(
                srcdoc = paste(readLines('highlight_q2.html'), collapse = '\n'),
                width = "100%",
                height = "600px",
                frameborder = "0"
              )
            })
          }
          
          else if (len == 1 & val == 1) {
            output$plot_issue_q2 <- renderPlot({
              issue_plot(result, token1, token2)
              
            })
          }
          
          else if (len == 1 & val == 2) {
            plot_sentiment(result, 'highlight_q2.html')
            
            getPage <- function() {
              return(includeHTML("highlight_q2.html"))
            }
            
            output$sentiment_q2 <- renderUI({
              #getPage()
              tags$iframe(
                srcdoc = paste(readLines('highlight_q2.html'), collapse = '\n'),
                width = "100%",
                height = "600px",
                frameborder = "0"
              )
            })
          }
          
        })
        
      }) # updating dashboard code ends here
    }
  })
  
  
  
}
shinyApp(ui, server)