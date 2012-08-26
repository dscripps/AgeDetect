//
//  DetailsViewController.m
//  AG02
//
//  Created by デービット スクリプス on 8/18/12.
//  Copyright (c) 2012 __MyCompanyName__. All rights reserved.
//

#import "DetailsViewController.h"
#import "ResultsViewController.h"

@interface DetailsViewController ()

@end

@implementation DetailsViewController

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        // Custom initialization
    }
    return self;
}

- (void)viewDidLoad
{
    [super viewDidLoad];
    // Do any additional setup after loading the view from its nib.
    

    
}

- (void)viewDidUnload
{
    [super viewDidUnload];
    // Release any retained subviews of the main view.
    // e.g. self.myOutlet = nil;
}
- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}

- (void) initStuff:(NSString*)part {
    //NSString *part = @"left_eye";
    //NSString *part = @"forehead";
    NSString *urlStr = [NSString stringWithFormat:@"http://ec2-176-34-8-245.ap-northeast-1.compute.amazonaws.com/uploads/%@_result%@.jpg", [[NSUserDefaults standardUserDefaults] stringForKey:@"uuid"], part];
    detailImageView.image = [UIImage imageWithData:[NSData dataWithContentsOfURL:[NSURL URLWithString:urlStr]]];
}


- (IBAction)returnButton:(id)sender
{
    ResultsViewController *cV = [[[ResultsViewController alloc] initWithNibName:@"ResultsViewController" bundle:nil] autorelease];
    cV.modalTransitionStyle = UIModalTransitionStyleCrossDissolve;
    [self presentModalViewController:cV animated:YES];
    [self viewDidUnload];
}


- (IBAction)saveButton:(id)sender
{
    NSLog(@"save button here");
}


@end
